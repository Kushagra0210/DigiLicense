/**
 * An opaque transaction scope supplied by a persistence adapter.
 *
 * Domain and application code may pass this value to transaction-scoped
 * repository ports, but cannot access an ORM client through it.
 */
export abstract class TransactionContext {
  protected constructor() {}

  protected transactionContextBrand(): void {}
}

export type TransactionOperation<TResult> = (
  context: TransactionContext,
) => Promise<TResult>;

/** Runs all persistence work in the callback in one physical transaction. */
export interface TransactionRunner {
  run<TResult>(operation: TransactionOperation<TResult>): Promise<TResult>;
}
