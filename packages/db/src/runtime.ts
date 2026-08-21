import type { TransactionRunner } from "@digilicense/backend-core";

import { getPrismaClient } from "./client";
import { PrismaTransactionRunner } from "./transaction-runner";

export interface DatabaseRuntimeOptions {
  databaseUrl: string;
  environment: "development" | "production" | "test";
  poolMax?: number;
  connectionTimeoutMs?: number;
  cache?: boolean;
}

export interface DatabaseRuntime {
  readonly transactionRunner: TransactionRunner;
  checkReadiness(): Promise<void>;
  disconnect(): Promise<void>;
}

export function createDatabaseRuntime(
  options: DatabaseRuntimeOptions,
): DatabaseRuntime {
  const client = getPrismaClient({
    databaseUrl: options.databaseUrl,
    environment: options.environment,
    poolMax: options.poolMax ?? 5,
    connectionTimeoutMs: options.connectionTimeoutMs ?? 5_000,
    cache: options.cache,
  });
  const transactionRunner = new PrismaTransactionRunner(client);

  return {
    transactionRunner,
    async checkReadiness(): Promise<void> {
      await client.$queryRaw`SELECT 1`;
    },
    async disconnect(): Promise<void> {
      await client.$disconnect();
    },
  };
}
