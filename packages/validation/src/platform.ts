import { z } from "zod";

export const requestIdSchema = z.string().uuid();

export const errorEnvelopeSchema = z
  .object({
    error: z
      .object({
        code: z.string().min(1),
        message: z.string().min(1),
        requestId: requestIdSchema,
      })
      .strict(),
  })
  .strict();

export const healthResponseSchema = z
  .object({
    status: z.literal("ok"),
    requestId: requestIdSchema,
  })
  .strict();

export const readinessResponseSchema = z
  .object({
    status: z.enum(["ready", "unavailable"]),
    requestId: requestIdSchema,
  })
  .strict();

export type ErrorEnvelope = z.infer<typeof errorEnvelopeSchema>;
export type HealthResponse = z.infer<typeof healthResponseSchema>;
export type ReadinessResponse = z.infer<typeof readinessResponseSchema>;
