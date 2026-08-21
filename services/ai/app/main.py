"""FastAPI application for the private DigiLicense AI boundary."""

from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.assistant_service import AssistantService
from app.config import Settings, get_settings
from app.dlp import PresidioDLPService
from app.intents import IntentRouter
from app.middleware import MaxBodySizeMiddleware, MetadataLoggingMiddleware, configure_logging
from app.models import AssistantRequest, AssistantResponse
from app.security import require_service_auth


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings.log_level)

    application = FastAPI(
        title="DigiLicense AI",
        summary="Private, stateless explanation service for the DigiLicense prototype",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    application.state.settings = resolved_settings
    application.state.assistant_service = AssistantService(
        dlp=PresidioDLPService(score_threshold=resolved_settings.dlp_score_threshold),
        router=IntentRouter(
            confidence_threshold=resolved_settings.intent_confidence_threshold,
        ),
    )
    application.add_middleware(MetadataLoggingMiddleware)
    application.add_middleware(
        MaxBodySizeMiddleware,
        max_body_bytes=resolved_settings.max_request_body_bytes,
    )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        # FastAPI's default error shape includes rejected input. Remove it so malformed requests
        # cannot echo sensitive values into responses or future error logging.
        errors = [
            {
                "location": list(error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"errors": errors},
        )

    @application.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "live"}

    @application.get(
        "/health/ready",
        tags=["health"],
        responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Not configured"}},
    )
    async def readiness() -> JSONResponse:
        if resolved_settings.service_api_key is None:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not_ready"},
            )
        return JSONResponse(content={"status": "ready"})

    @application.post(
        "/v1/assistant/messages",
        response_model=AssistantResponse,
        response_model_by_alias=True,
        tags=["assistant"],
        dependencies=[Depends(require_service_auth)],
        responses={
            status.HTTP_401_UNAUTHORIZED: {"description": "Invalid service credentials"},
            status.HTTP_413_CONTENT_TOO_LARGE: {"description": "Request body too large"},
            status.HTTP_422_UNPROCESSABLE_CONTENT: {"description": "Invalid request"},
            status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Service is not configured"},
        },
    )
    async def assistant_message(
        request: Request,
        payload: Annotated[AssistantRequest, Depends(validate_configured_question_limit)],
    ) -> AssistantResponse:
        assistant_service: AssistantService = request.app.state.assistant_service
        return assistant_service.answer(payload)

    return application


async def validate_configured_question_limit(
    request: Request,
    payload: AssistantRequest,
) -> AssistantRequest:
    settings: Settings = request.app.state.settings
    if len(payload.question) > settings.max_question_chars:
        raise RequestValidationError(
            [
                {
                    "type": "string_too_long",
                    "loc": ("body", "question"),
                    "msg": (
                        "Question must contain at most "
                        f"{settings.max_question_chars} characters"
                    ),
                    "ctx": {"max_length": settings.max_question_chars},
                    "input": "[REDACTED]",
                }
            ]
        )
    return payload


app = create_app()
