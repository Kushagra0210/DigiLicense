import { z } from "zod";
import { describe, expect, it } from "vitest";

import { GET as getHealth } from "../../apps/web/src/app/api/health/route";
import { parseJsonBody } from "../../apps/web/src/server/http/json-body";
import {
  errorResponse,
  HttpTransportError,
} from "../../apps/web/src/server/http/response";

describe("HTTP foundation", () => {
  it("returns liveness with a server-generated correlation ID", async () => {
    const response = getHealth();
    const body = (await response.json()) as {
      status: string;
      requestId: string;
    };

    expect(response.status).toBe(200);
    expect(body.status).toBe("ok");
    expect(body.requestId).toBe(response.headers.get("x-request-id"));
    expect(body.requestId).toMatch(/^[0-9a-f-]{36}$/i);
    expect(response.headers.get("cache-control")).toBe("no-store");
  });

  it("validates a bounded JSON body", async () => {
    const request = new Request("https://example.test/api/example", {
      method: "POST",
      body: JSON.stringify({ name: "Sarathi" }),
      headers: { "content-type": "application/json" },
    });

    await expect(
      parseJsonBody(request, z.object({ name: z.string() }), 128),
    ).resolves.toEqual({ name: "Sarathi" });
  });

  it("rejects oversized bodies before validation", async () => {
    const request = new Request("https://example.test/api/example", {
      method: "POST",
      body: JSON.stringify({ value: "x".repeat(80) }),
    });

    await expect(parseJsonBody(request, z.unknown(), 32)).rejects.toMatchObject({
      status: 413,
      code: "REQUEST_TOO_LARGE",
    });
  });

  it("maps unknown failures to a generic public envelope", async () => {
    const requestId = crypto.randomUUID();
    const response = errorResponse(new Error("database password leaked"), {
      requestId,
    });
    const serialized = JSON.stringify(await response.json());

    expect(response.status).toBe(500);
    expect(serialized).toContain("INTERNAL_ERROR");
    expect(serialized).toContain(requestId);
    expect(serialized).not.toContain("database password leaked");
  });

  it("preserves only explicitly public transport errors", async () => {
    const requestId = crypto.randomUUID();
    const response = errorResponse(
      new HttpTransportError(400, "VALIDATION_FAILED", "The request is invalid."),
      { requestId },
    );

    expect(response.status).toBe(400);
    await expect(response.json()).resolves.toMatchObject({
      error: { code: "VALIDATION_FAILED", requestId },
    });
  });
});
