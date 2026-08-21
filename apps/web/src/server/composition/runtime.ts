import "server-only";

import {
  createDatabaseRuntime,
  type DatabaseRuntime,
} from "@digilicense/db";

import { getServerEnvironment } from "../config/env";

let databaseRuntime: DatabaseRuntime | undefined;

export function getDatabaseRuntime(): DatabaseRuntime {
  if (databaseRuntime) {
    return databaseRuntime;
  }

  const environment = getServerEnvironment();
  databaseRuntime = createDatabaseRuntime({
    databaseUrl: environment.DATABASE_URL,
    environment: environment.NODE_ENV,
    poolMax: environment.DATABASE_POOL_MAX,
    connectionTimeoutMs: environment.DATABASE_CONNECTION_TIMEOUT_MS,
  });

  return databaseRuntime;
}
