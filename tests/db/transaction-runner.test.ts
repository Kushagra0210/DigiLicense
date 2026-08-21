import type { Prisma, PrismaClient } from "../../packages/db/src/generated/prisma/client";
import { describe, expect, it } from "vitest";

import {
  PrismaTransactionRunner,
  requirePrismaTransactionClient,
} from "../../packages/db/src/transaction-runner";

describe("Prisma transaction runner", () => {
  it("binds one opaque context and propagates callback failure", async () => {
    const transactionClient = {} as Prisma.TransactionClient;
    let transactionCalls = 0;
    const client = {
      $transaction: async <T>(
        operation: (transaction: Prisma.TransactionClient) => Promise<T>,
      ): Promise<T> => {
        transactionCalls += 1;
        return operation(transactionClient);
      },
    } as unknown as PrismaClient;
    const runner = new PrismaTransactionRunner(client);
    const failure = new Error("rollback");

    await expect(
      runner.run(async (context) => {
        expect(requirePrismaTransactionClient(context)).toBe(transactionClient);
        throw failure;
      }),
    ).rejects.toBe(failure);
    expect(transactionCalls).toBe(1);
  });
});
