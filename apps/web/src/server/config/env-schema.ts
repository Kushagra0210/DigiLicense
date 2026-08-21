import { z } from "zod";

const postgresUrlSchema = z.string().url().superRefine((value, context) => {
  let protocol: string;
  try {
    protocol = new URL(value).protocol;
  } catch {
    return;
  }

  if (protocol !== "postgres:" && protocol !== "postgresql:") {
    context.addIssue({
      code: "custom",
      message: "must use the postgres or postgresql protocol",
    });
  }
});

export const serverEnvironmentSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: postgresUrlSchema,
  DATABASE_POOL_MAX: z.coerce.number().int().min(1).max(20).default(5),
  DATABASE_CONNECTION_TIMEOUT_MS: z.coerce
    .number()
    .int()
    .min(100)
    .max(30_000)
    .default(5_000),
});

export type ServerEnvironment = z.infer<typeof serverEnvironmentSchema>;

export class ServerEnvironmentError extends Error {
  constructor(readonly fields: readonly string[]) {
    super(`Invalid server configuration: ${fields.join(", ")}`);
    this.name = "ServerEnvironmentError";
  }
}

export function parseServerEnvironment(
  source: NodeJS.ProcessEnv,
): ServerEnvironment {
  const result = serverEnvironmentSchema.safeParse(source);

  if (!result.success) {
    const fields = [
      ...new Set(result.error.issues.map((issue) => issue.path.join("."))),
    ];
    throw new ServerEnvironmentError(fields);
  }

  return result.data;
}
