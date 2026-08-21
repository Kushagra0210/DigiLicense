import type { ErrorEnvelope } from "@digilicense/validation";

import type { RequestContext } from "./request-context";

export function jsonResponse(
  body: unknown,
  context: RequestContext,
  init: ResponseInit = {},
): Response {
  const headers = new Headers(init.headers);
  headers.set("cache-control", "no-store");
  headers.set("content-type", "application/json; charset=utf-8");
  headers.set("x-request-id", context.requestId);

  return new Response(JSON.stringify(body), { ...init, headers });
}

export class HttpTransportError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    readonly publicMessage: string,
  ) {
    super(publicMessage);
    this.name = "HttpTransportError";
  }
}

export function errorResponse(
  error: unknown,
  context: RequestContext,
): Response {
  const knownError =
    error instanceof HttpTransportError
      ? error
      : new HttpTransportError(
          500,
          "INTERNAL_ERROR",
          "The request could not be completed.",
        );
  const body: ErrorEnvelope = {
    error: {
      code: knownError.code,
      message: knownError.publicMessage,
      requestId: context.requestId,
    },
  };

  return jsonResponse(body, context, { status: knownError.status });
}
