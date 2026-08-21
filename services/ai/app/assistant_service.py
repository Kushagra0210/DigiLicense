"""Safety-first orchestration for deterministic assistant responses."""

import logging

from app.dlp import PresidioDLPService
from app.intents import IntentRouter
from app.intents.catalog import (
    PII_BLOCK_GUIDANCE,
    SAFETY_FAILURE_GUIDANCE,
    Guidance,
    guidance_for,
)
from app.models import AssistantRequest, AssistantResponse, ProviderResult
from app.models.enums import BlockedReason, DLPAction, Intent, Locale

LOGGER = logging.getLogger("digilicense.ai.safety")


class AssistantService:
    def __init__(self, dlp: PresidioDLPService, router: IntentRouter) -> None:
        self.dlp = dlp
        self.router = router

    def answer(self, request: AssistantRequest) -> AssistantResponse:
        try:
            inspection = self.dlp.inspect(request.question)
        except Exception as error:  # fail closed at the security boundary
            self._log_safety_failure("inbound", error)
            return self._safety_failure(request.locale)

        if inspection.result.action is DLPAction.BLOCK_PII:
            return self._pii_block(request.locale)

        route = self.router.route(
            inspection.normalized_text,
            page=request.page,
            reason_code=request.reason_code,
        )
        guidance = guidance_for(route.intent, request.locale)
        response = AssistantResponse(
            answer=guidance.answer,
            sourceIds=[],
            uncertain=route.intent is Intent.UNSUPPORTED,
            escalation=guidance.escalation,
            fallbackUsed=True,
            blockedReason=(
                BlockedReason.UNSUPPORTED_REQUEST
                if route.intent is Intent.UNSUPPORTED
                else None
            ),
        )
        return self.protect_outbound(response, request.locale)

    def finalize_provider_result(
        self,
        result: ProviderResult,
        locale: Locale,
    ) -> AssistantResponse:
        """Future provider adapters must pass their result through this boundary."""

        candidate = AssistantResponse(
            answer=result.answer,
            sourceIds=result.source_ids,
            uncertain=result.uncertain,
            escalation=result.escalation,
            fallbackUsed=False,
            blockedReason=None,
        )
        return self.protect_outbound(candidate, locale)

    def protect_outbound(
        self,
        response: AssistantResponse,
        locale: Locale,
    ) -> AssistantResponse:
        outbound_parts = [response.answer, *response.source_ids]
        if response.escalation is not None:
            outbound_parts.append(response.escalation)
        outbound_text = " ".join(outbound_parts)
        try:
            inspection = self.dlp.inspect(outbound_text)
        except Exception as error:
            self._log_safety_failure("outbound", error)
            return self._safety_failure(locale)
        if inspection.result.action is DLPAction.BLOCK_PII:
            return self._pii_block(locale)
        return response

    @staticmethod
    def _from_guidance(
        guidance: Guidance,
        blocked_reason: BlockedReason,
    ) -> AssistantResponse:
        return AssistantResponse(
            answer=guidance.answer,
            sourceIds=[],
            uncertain=True,
            escalation=guidance.escalation,
            fallbackUsed=True,
            blockedReason=blocked_reason,
        )

    def _pii_block(self, locale: Locale) -> AssistantResponse:
        return self._from_guidance(PII_BLOCK_GUIDANCE[locale], BlockedReason.PII_DETECTED)

    def _safety_failure(self, locale: Locale) -> AssistantResponse:
        return self._from_guidance(
            SAFETY_FAILURE_GUIDANCE[locale],
            BlockedReason.SAFETY_CHECK_UNAVAILABLE,
        )

    @staticmethod
    def _log_safety_failure(stage: str, error: Exception) -> None:
        # Log only the error class. Third-party exception messages may contain analyzed text.
        LOGGER.error(
            "safety_check_failed stage=%s error_type=%s",
            stage,
            type(error).__name__,
        )
