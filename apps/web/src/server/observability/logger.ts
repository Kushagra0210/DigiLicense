export type SafeLogLevel = "info" | "warn" | "error";
export type SafeLogEventName =
  | "request.completed"
  | "request.failed"
  | "dependency.failed";

export interface SafeLogEvent {
  level: SafeLogLevel;
  event: SafeLogEventName;
  requestId: string;
  operation?: string;
  route?: string;
  outcome?: "success" | "failure";
  errorCode?: string;
  durationMs?: number;
}

export function toSafeLogRecord(event: SafeLogEvent): Record<string, unknown> {
  const record: Record<string, unknown> = {
    timestamp: new Date().toISOString(),
    level: event.level,
    event: event.event,
    requestId: event.requestId,
  };

  if (event.operation !== undefined) record.operation = event.operation;
  if (event.route !== undefined) record.route = event.route;
  if (event.outcome !== undefined) record.outcome = event.outcome;
  if (event.errorCode !== undefined) record.errorCode = event.errorCode;
  if (event.durationMs !== undefined) record.durationMs = event.durationMs;

  return record;
}

export function writeSafeLog(event: SafeLogEvent): void {
  const line = JSON.stringify(toSafeLogRecord(event));

  if (event.level === "error") {
    console.error(line);
    return;
  }

  if (event.level === "warn") {
    console.warn(line);
    return;
  }

  console.info(line);
}
