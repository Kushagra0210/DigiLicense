import "server-only";

import {
  parseServerEnvironment,
  type ServerEnvironment,
} from "./env-schema";

let cachedEnvironment: ServerEnvironment | undefined;

export function getServerEnvironment(): ServerEnvironment {
  cachedEnvironment ??= parseServerEnvironment(process.env);
  return cachedEnvironment;
}
