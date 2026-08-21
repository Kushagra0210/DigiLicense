import { describe, expect, it } from "vitest";

import {
  parseServerEnvironment,
  ServerEnvironmentError,
} from "../../apps/web/src/server/config/env-schema";

describe("server environment", () => {
  it("parses PostgreSQL configuration and applies bounded defaults", () => {
    expect(
      parseServerEnvironment({
        DATABASE_URL: "postgresql://user:password@db.example.test/app?sslmode=require",
        NODE_ENV: "test",
      }),
    ).toEqual({
      DATABASE_URL: "postgresql://user:password@db.example.test/app?sslmode=require",
      NODE_ENV: "test",
      DATABASE_POOL_MAX: 5,
      DATABASE_CONNECTION_TIMEOUT_MS: 5_000,
    });
  });

  it("fails clearly without echoing a secret value", () => {
    const secret = "not-a-postgres-secret";
    expect(() =>
      parseServerEnvironment({ DATABASE_URL: secret, NODE_ENV: "production" }),
    ).toThrow(ServerEnvironmentError);

    try {
      parseServerEnvironment({ DATABASE_URL: secret, NODE_ENV: "production" });
    } catch (error) {
      expect(String(error)).toContain("DATABASE_URL");
      expect(String(error)).not.toContain(secret);
    }
  });
});
