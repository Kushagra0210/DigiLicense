/**
 * The single application-use-case contract used beneath every transport.
 * Route Handlers and Server Actions adapt transport concerns to this shape.
 */
export interface UseCase<TInput, TOutput, TContext = undefined> {
  execute(
    input: TInput,
    ...context: [TContext] extends [undefined]
      ? []
      : [context: TContext]
  ): Promise<TOutput>;
}
