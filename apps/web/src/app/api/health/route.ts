import type { HealthResponse } from "@digilicense/validation";

import { createRequestContext } from "../../../server/http/request-context";
import { jsonResponse } from "../../../server/http/response";

export function GET(): Response {
  const context = createRequestContext();
  const body: HealthResponse = {
    status: "ok",
    requestId: context.requestId,
  };

  return jsonResponse(body, context);
}
