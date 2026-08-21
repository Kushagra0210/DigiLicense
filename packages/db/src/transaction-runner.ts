import {
  TransactionContext,
  type TransactionOperation,
  type TransactionRunner,
} from "@digilicense/backend-core";

import type { Prisma, PrismaClient } from "./generated/prisma/client";

export class PrismaTransactionContext extends TransactionContext {
  constructor(readonly client: Prisma.TransactionClient) {
    super();
  }
}

export function requirePrismaTransactionClient(
  context: TransactionContext,
): Prisma.TransactionClient {
  if (!(context instanceof PrismaTransactionContext)) {
    throw new Error("A Prisma repository received an incompatible transaction context.");
  }

  return context.client;
}

export class PrismaTransactionRunner implements TransactionRunner {
  constructor(private readonly client: PrismaClient) {}

  run<TResult>(operation: TransactionOperation<TResult>): Promise<TResult> {
    return this.client.$transaction((transaction) =>
      operation(new PrismaTransactionContext(transaction)),
    );
  }
}
