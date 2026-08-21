"""Boundary middleware with bounded bodies and metadata-only logging."""

import logging
import time

from starlette.types import ASGIApp, Message, Receive, Scope, Send

LOGGER = logging.getLogger("digilicense.ai.requests")
SAFE_ROUTE_LABELS = {
    "/health/live": "health_live",
    "/health/ready": "health_ready",
    "/v1/assistant/messages": "assistant_messages",
}


class MaxBodySizeMiddleware:
    """Reject oversized HTTP bodies even when Content-Length is missing or incorrect."""

    def __init__(self, app: ASGIApp, max_body_bytes: int) -> None:
        self.app = app
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        content_length = self._content_length(scope)
        if content_length is not None and content_length > self.max_body_bytes:
            await self._send_too_large(send)
            return

        consumed = 0
        exceeded = False

        async def limited_receive() -> Message:
            nonlocal consumed, exceeded
            message = await receive()
            if message["type"] == "http.request":
                consumed += len(message.get("body", b""))
                if consumed > self.max_body_bytes:
                    exceeded = True
                    return {"type": "http.disconnect"}
            return message

        response_started = False

        async def guarded_send(message: Message) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, limited_receive, guarded_send)
        except Exception:
            if exceeded and not response_started:
                await self._send_too_large(send)
                return
            raise

    @staticmethod
    def _content_length(scope: Scope) -> int | None:
        for name, value in scope.get("headers", []):
            if name.lower() == b"content-length":
                try:
                    return int(value)
                except ValueError:
                    return None
        return None

    @staticmethod
    async def _send_too_large(send: Send) -> None:
        body = b'{"detail":"Request body too large"}'
        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode("ascii")),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})


class MetadataLoggingMiddleware:
    """Log request metadata only; never inspect headers, query strings, or bodies."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        started_at = time.perf_counter()
        status_code = 500

        async def capture_status(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
            await send(message)

        try:
            await self.app(scope, receive, capture_status)
        finally:
            duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
            route_label = SAFE_ROUTE_LABELS.get(scope.get("path", ""), "unmatched")
            LOGGER.info(
                "http_request method=%s route=%s status=%s duration_ms=%s",
                scope.get("method", "UNKNOWN"),
                route_label,
                status_code,
                duration_ms,
            )


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    # Uvicorn's default access logger includes the attacker-controlled raw path. The sanitized
    # metadata logger above is the only request logger permitted for this service.
    logging.getLogger("uvicorn.access").disabled = True
