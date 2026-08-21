import logging

import pytest

from app.assistant_service import AssistantService
from app.dlp import PresidioDLPService
from app.intents import IntentRouter
from app.intents.catalog import guidance_for
from app.models import AssistantRequest, ProviderResult
from app.models.enums import BlockedReason, Intent, Locale


class FailingDLP:
    def inspect(self, _text: str) -> None:
        raise RuntimeError("PRIVATE_FAILURE_MARKER")


class SpyRouter(IntentRouter):
    def __init__(self) -> None:
        super().__init__()
        self.call_count = 0

    def route(self, *args: object, **kwargs: object):  # type: ignore[no-untyped-def]
        self.call_count += 1
        return super().route(*args, **kwargs)  # type: ignore[arg-type]


def request_with_question(question: str, locale: str = "en") -> AssistantRequest:
    return AssistantRequest(
        question=question,
        locale=locale,
        service="driving_licence",
        page="appointment_waitlist",
    )


def test_pii_is_blocked_before_intent_routing() -> None:
    router = SpyRouter()
    service = AssistantService(PresidioDLPService(), router)
    raw_value = "60000 00000"

    response = service.answer(request_with_question(f"My mobile is {raw_value}"))

    assert response.blocked_reason is BlockedReason.PII_DETECTED
    assert router.call_count == 0
    assert raw_value not in response.answer
    assert raw_value not in (response.escalation or "")


@pytest.mark.parametrize("locale", ["en", "hi"])
def test_bilingual_pii_block_message_contains_no_detected_value(locale: str) -> None:
    service = AssistantService(PresidioDLPService(), IntentRouter())
    raw_value = "918273"

    response = service.answer(request_with_question(f"OTP is {raw_value}", locale))

    assert response.blocked_reason is BlockedReason.PII_DETECTED
    assert raw_value not in response.answer
    assert response.fallback_used is True


def test_dlp_failure_fails_closed_without_logging_exception_message(
    caplog: pytest.LogCaptureFixture,
) -> None:
    service = AssistantService(FailingDLP(), IntentRouter())  # type: ignore[arg-type]

    with caplog.at_level(logging.ERROR, logger="digilicense.ai.safety"):
        response = service.answer(request_with_question("PRIVATE_QUESTION_MARKER"))

    assert response.blocked_reason is BlockedReason.SAFETY_CHECK_UNAVAILABLE
    assert "PRIVATE_QUESTION_MARKER" not in response.answer
    assert "PRIVATE_FAILURE_MARKER" not in caplog.text
    assert "error_type=RuntimeError" in caplog.text


def test_fake_provider_pii_is_replaced_by_safe_outbound_fallback() -> None:
    service = AssistantService(PresidioDLPService(), IntentRouter())
    leaked_value = "918273"
    fake_result = ProviderResult(
        answer=f"Your OTP is {leaked_value}",
        sourceIds=[],
        uncertain=False,
        escalation=None,
    )

    response = service.finalize_provider_result(fake_result, Locale.ENGLISH)

    assert response.blocked_reason is BlockedReason.PII_DETECTED
    assert response.fallback_used is True
    assert leaked_value not in response.answer


@pytest.mark.parametrize(
    "leaked_output",
    [
        "Aadhaar 2345 6789 0123",
        "PAN ZZZPZ9999Z",
        "Passport Z99 99991",
        "Voter ID ZZZ9999999",
        "Mobile 60000 00000",
        "OTP 918273",
        "Driving licence DL1420260000001",
        "Application number APP202600001",
        "Receipt RCP20260001",
        "Vehicle number DL-00-XX-0000",
        "UPI pii.fixture@okaxis",
        "IFSC TEST0123456",
        "Bank account 999900000000",
        "Card 4111 1111 1111 1111",
        "CVV 987",
        "My address is 999 Synthetic Test Road",
        "My name is Synthetic Applicant",
    ],
)
def test_every_critical_provider_leak_is_blocked(leaked_output: str) -> None:
    service = AssistantService(PresidioDLPService(), IntentRouter())

    response = service.finalize_provider_result(
        ProviderResult(
            answer=leaked_output,
            sourceIds=[],
            uncertain=False,
            escalation=None,
        ),
        Locale.ENGLISH,
    )

    assert response.blocked_reason is BlockedReason.PII_DETECTED
    assert leaked_output not in response.answer


def test_provider_source_ids_are_included_in_outbound_dlp() -> None:
    service = AssistantService(PresidioDLPService(), IntentRouter())
    response = service.finalize_provider_result(
        ProviderResult(
            answer="Safe answer",
            sourceIds=["OTP-918273"],
            uncertain=False,
            escalation=None,
        ),
        Locale.ENGLISH,
    )

    assert response.blocked_reason is BlockedReason.PII_DETECTED
    assert response.source_ids == []


def test_outbound_dlp_failure_also_fails_closed() -> None:
    service = AssistantService(FailingDLP(), IntentRouter())  # type: ignore[arg-type]
    response = service.finalize_provider_result(
        ProviderResult(
            answer="Safe-looking output",
            sourceIds=[],
            uncertain=False,
            escalation=None,
        ),
        Locale.ENGLISH,
    )

    assert response.blocked_reason is BlockedReason.SAFETY_CHECK_UNAVAILABLE


@pytest.mark.parametrize("locale", list(Locale))
@pytest.mark.parametrize("intent", list(Intent))
def test_reviewed_fallback_catalog_passes_outbound_dlp(
    locale: Locale,
    intent: Intent,
) -> None:
    service = AssistantService(PresidioDLPService(), IntentRouter())
    guidance = guidance_for(intent, locale)

    response = service.finalize_provider_result(
        ProviderResult(
            answer=guidance.answer,
            sourceIds=[],
            uncertain=intent is Intent.UNSUPPORTED,
            escalation=guidance.escalation,
        ),
        locale,
    )

    assert response.blocked_reason is None
