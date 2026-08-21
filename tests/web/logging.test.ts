import { describe, expect, it } from "vitest";

import {
  toSafeLogRecord,
  type SafeLogEvent,
} from "../../apps/web/src/server/observability/logger";

describe("safe structured logging", () => {
  it("keeps only the allowlisted diagnostic fields", () => {
    const record = toSafeLogRecord({
      level: "error",
      event: "dependency.failed",
      requestId: crypto.randomUUID(),
      route: "/api/readiness",
      operation: "database.readiness",
      outcome: "failure",
      errorCode: "DATABASE_UNAVAILABLE",
      authorization: "Bearer secret",
      cookie: "session=secret",
      databaseUrl: "postgresql://secret",
    } as SafeLogEvent & Record<string, unknown>);

    expect(record).toMatchObject({
      level: "error",
      event: "dependency.failed",
      route: "/api/readiness",
      operation: "database.readiness",
      outcome: "failure",
      errorCode: "DATABASE_UNAVAILABLE",
    });
    expect(record).not.toHaveProperty("authorization");
    expect(record).not.toHaveProperty("cookie");
    expect(record).not.toHaveProperty("databaseUrl");
  });
});
