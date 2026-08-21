import { z } from "zod";

import { HttpTransportError } from "./response";

export const DEFAULT_JSON_BODY_LIMIT_BYTES = 64 * 1024;

async function readBoundedBody(request: Request, limitBytes: number): Promise<string> {
  const declaredLength = request.headers.get("content-length");
  if (declaredLength !== null) {
    const parsedLength = Number(declaredLength);
    if (!Number.isSafeInteger(parsedLength) || parsedLength < 0) {
      throw new HttpTransportError(400, "INVALID_CONTENT_LENGTH", "The request is invalid.");
    }
    if (parsedLength > limitBytes) {
      throw new HttpTransportError(413, "REQUEST_TOO_LARGE", "The request body is too large.");
    }
  }

  if (!request.body) {
    throw new HttpTransportError(400, "INVALID_JSON", "A JSON request body is required.");
  }

  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let totalBytes = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    totalBytes += value.byteLength;
    if (totalBytes > limitBytes) {
      await reader.cancel();
      throw new HttpTransportError(413, "REQUEST_TOO_LARGE", "The request body is too large.");
    }
    chunks.push(value);
  }

  const body = new Uint8Array(totalBytes);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }

  return new TextDecoder("utf-8", { fatal: true }).decode(body);
}

export async function parseJsonBody<TSchema extends z.ZodType>(
  request: Request,
  schema: TSchema,
  limitBytes = DEFAULT_JSON_BODY_LIMIT_BYTES,
): Promise<z.output<TSchema>> {
  let payload: unknown;

  try {
    payload = JSON.parse(await readBoundedBody(request, limitBytes));
  } catch (error) {
    if (error instanceof HttpTransportError) throw error;
    throw new HttpTransportError(400, "INVALID_JSON", "The request body must be valid JSON.");
  }

  const result = schema.safeParse(payload);
  if (!result.success) {
    throw new HttpTransportError(400, "VALIDATION_FAILED", "The request is invalid.");
  }

  return result.data;
}
