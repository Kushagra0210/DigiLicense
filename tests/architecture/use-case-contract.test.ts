import { describe, expect, it } from "vitest";

import type { UseCase } from "../../packages/backend-core/src/use-case";

describe("UseCase context contract", () => {
  it("supports natural calls for context-free and context-required use cases", async () => {
    const contextFreeUseCase: UseCase<string, string> = {
      async execute(input) {
        return input.toUpperCase();
      },
    };
    const contextRequiredUseCase: UseCase<
      string,
      string,
      { prefix: string }
    > = {
      async execute(input, context) {
        return `${context.prefix}${input}`;
      },
    };

    await expect(contextFreeUseCase.execute("input")).resolves.toBe("INPUT");
    await expect(
      contextRequiredUseCase.execute("input", { prefix: "safe-" }),
    ).resolves.toBe("safe-input");

    if (false) {
      // @ts-expect-error A context-free use case does not accept a context argument.
      void contextFreeUseCase.execute("input", undefined);
      // @ts-expect-error A context-required use case cannot omit its context.
      void contextRequiredUseCase.execute("input");
    }
  });
});
