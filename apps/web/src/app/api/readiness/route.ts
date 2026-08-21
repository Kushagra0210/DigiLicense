import type { ReadinessResponse } from "@digilicense/validation";

import { getDatabaseRuntime } from "../../../server/composition/runtime";
import { createRequestContext } from "../../../server/http/request-context";
import { jsonResponse } from "../../../server/http/response";
import { writeSafeLog } from "../../../server/observability/logger";

export async function GET(): Promise<Response> {
  const context = createRequestContext();
  const startedAt = performance.now();

  try {
    await getDatabaseRuntime().checkReadiness();
    const body: ReadinessResponse = {
      status: "ready",
      requestId: context.requestId,
    };
    writeSafeLog({
      level: "info",
      event: "request.completed",
      requestId: context.requestId,
      route: "/api/readiness",
      operation: "readiness.check",
      outcome: "success",
      durationMs: Math.round(performance.now() - startedAt),
    });
    return jsonResponse(body, context);
  } catch {
    const body: ReadinessResponse = {
      status: "unavailable",
      requestId: context.requestId,
    };
    writeSafeLog({
      level: "error",
      event: "dependency.failed",
      requestId: context.requestId,
      route: "/api/readiness",
      operation: "database.readiness",
      outcome: "failure",
      errorCode: "DATABASE_UNAVAILABLE",
      durationMs: Math.round(performance.now() - startedAt),
    });
    return jsonResponse(body, context, { status: 503 });
  }
}
