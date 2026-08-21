import { afterAll, beforeAll, describe, expect, it } from "vitest";

import { getPrismaClient } from "../../packages/db/src/client";
import {
  PrismaTransactionRunner,
  requirePrismaTransactionClient,
} from "../../packages/db/src/transaction-runner";

const testDatabaseUrl = process.env.TEST_DATABASE_URL;

describe.skipIf(!testDatabaseUrl)("Prisma transaction integration", () => {
  let client: ReturnType<typeof getPrismaClient>;
  let runner: PrismaTransactionRunner;

  beforeAll(() => {
    if (!testDatabaseUrl) throw new Error("TEST_DATABASE_URL is required.");

    client = getPrismaClient({
      databaseUrl: testDatabaseUrl,
      environment: "test",
      poolMax: 1,
      connectionTimeoutMs: 5_000,
      cache: false,
    });
    runner = new PrismaTransactionRunner(client);
  });

  afterAll(async () => {
    await client.$disconnect();
  });

  it("commits successful transaction work", async () => {
    try {
      await runner.run(async (context) => {
        const transaction = requirePrismaTransactionClient(context);
        await transaction.$executeRaw`CREATE TEMP TABLE phase_0_commit_probe (value integer NOT NULL)`;
        await transaction.$executeRaw`INSERT INTO phase_0_commit_probe (value) VALUES (1)`;
      });

      const rows = await client.$queryRaw<Array<{ value: number }>>`
        SELECT value FROM phase_0_commit_probe
      `;
      expect(rows).toEqual([{ value: 1 }]);
    } finally {
      await client.$executeRaw`DROP TABLE IF EXISTS phase_0_commit_probe`;
    }
  });

  it("rolls back when the transaction callback throws", async () => {
    const failure = new Error("intentional rollback");

    await expect(
      runner.run(async (context) => {
        const transaction = requirePrismaTransactionClient(context);
        await transaction.$executeRaw`CREATE TEMP TABLE phase_0_rollback_probe (value integer NOT NULL)`;
        await transaction.$executeRaw`INSERT INTO phase_0_rollback_probe (value) VALUES (1)`;
        throw failure;
      }),
    ).rejects.toBe(failure);

    const result = await client.$queryRaw<
      Array<{ relation_name: string | null }>
    >`SELECT to_regclass('pg_temp.phase_0_rollback_probe')::text AS relation_name`;
    expect(result).toEqual([{ relation_name: null }]);
  });

  it("rolls back multiple writes in the same scoped transaction", async () => {
    await client.$executeRaw`CREATE TEMP TABLE phase_0_multi_write_probe (value integer NOT NULL)`;

    try {
      await expect(
        runner.run(async (context) => {
          const transaction = requirePrismaTransactionClient(context);
          await transaction.$executeRaw`INSERT INTO phase_0_multi_write_probe (value) VALUES (1)`;
          await transaction.$executeRaw`INSERT INTO phase_0_multi_write_probe (value) VALUES (2)`;
          throw new Error("rollback both writes");
        }),
      ).rejects.toThrow("rollback both writes");

      const result = await client.$queryRaw<Array<{ count: bigint }>>`
        SELECT COUNT(*)::bigint AS count FROM phase_0_multi_write_probe
      `;
      expect(result).toEqual([{ count: 0n }]);
    } finally {
      await client.$executeRaw`DROP TABLE IF EXISTS phase_0_multi_write_probe`;
    }
  });
});
