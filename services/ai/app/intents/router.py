"""Rule-based routing into a fixed, non-executable intent catalog."""

from dataclasses import dataclass

from app.models.enums import Intent, Page, ReasonCode
from app.normalization import NormalizedText


@dataclass(frozen=True, slots=True)
class IntentRoute:
    intent: Intent
    confidence: float
    provider_eligible: bool


REASON_INTENTS = {
    ReasonCode.ACTION_LOCKED: Intent.LOCKED_ACTION,
    ReasonCode.WAITING_PERIOD_ACTIVE: Intent.WAITING_PERIOD,
    ReasonCode.LEARNER_LICENCE_EXPIRING: Intent.LEARNER_LICENCE_EXPIRY,
    ReasonCode.NO_MATCHING_SLOT: Intent.NO_APPOINTMENT_AVAILABLE,
    ReasonCode.WAITLIST_ACTIVE: Intent.WAITLIST_EXPLANATION,
    ReasonCode.OFFER_EXPIRING: Intent.OFFER_EXPIRY,
    ReasonCode.SIMULATED_ACTION: Intent.MOCK_VS_REAL,
    ReasonCode.CHECKLIST_REQUIRED: Intent.PREPARATION_CHECKLIST,
}

PAGE_INTENTS = {
    Page.DASHBOARD: Intent.CURRENT_STEP,
    Page.WAITING_PERIOD: Intent.WAITING_PERIOD,
    Page.APPOINTMENT_WAITLIST: Intent.WAITLIST_EXPLANATION,
    Page.APPOINTMENT_OFFER: Intent.OFFER_EXPIRY,
    Page.APPOINTMENT_CONFIRMED: Intent.PREPARATION_CHECKLIST,
}

INTENT_SIGNALS = {
    Intent.CURRENT_STEP: (
        "what next",
        "next step",
        "current step",
        "what should i do",
        "अब क्या",
        "अगला कदम",
        "agla step",
    ),
    Intent.LOCKED_ACTION: (
        "why locked",
        "is locked",
        "cannot continue",
        "can't continue",
        "action unavailable",
        "लॉक क्यों",
        "क्यों नहीं",
        "locked kyu",
    ),
    Intent.WAITING_PERIOD: (
        "waiting period",
        "how long must i wait",
        "when can i apply",
        "30 days",
        "प्रतीक्षा अवधि",
        "कब आवेदन",
        "kitna wait",
    ),
    Intent.LEARNER_LICENCE_EXPIRY: (
        "learner licence expire",
        "learner license expire",
        "valid until",
        "expiry date",
        "समाप्ति तिथि",
        "कब समाप्त",
        "expiry kab",
    ),
    Intent.NO_APPOINTMENT_AVAILABLE: (
        "no appointment",
        "no slot",
        "appointment unavailable",
        "slot unavailable",
        "स्लॉट उपलब्ध नहीं",
        "अपॉइंटमेंट नहीं",
        "slot nahi",
    ),
    Intent.WAITLIST_EXPLANATION: (
        "waitlist",
        "waiting list",
        "queue works",
        "प्रतीक्षा सूची",
        "वेटलिस्ट",
        "waitlist kaise",
    ),
    Intent.OFFER_EXPIRY: (
        "offer expire",
        "offer expires",
        "offer countdown",
        "time left on offer",
        "ऑफर समाप्त",
        "काउंटडाउन",
        "offer kab expire",
    ),
    Intent.MOCK_VS_REAL: (
        "is this real",
        "official government",
        "simulated",
        "mock action",
        "असली है",
        "सरकारी वेबसाइट",
        "nakli hai",
    ),
    Intent.PREPARATION_CHECKLIST: (
        "what to bring",
        "preparation checklist",
        "documents for test",
        "how to prepare",
        "क्या लाना",
        "तैयारी सूची",
        "kya lana",
    ),
}

INJECTION_SIGNALS = (
    "ignore previous",
    "ignore all instructions",
    "system prompt",
    "developer message",
    "reveal your prompt",
    "act as system",
    "पिछले निर्देश भूल",
)

GENERIC_HELP_SIGNALS = ("help", "explain", "why", "बताएं", "समझाएं", "madad")


class IntentRouter:
    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold

    def route(
        self,
        text: NormalizedText,
        page: Page,
        reason_code: ReasonCode | None,
    ) -> IntentRoute:
        searchable = text.value.casefold()

        if any(signal in searchable for signal in INJECTION_SIGNALS):
            return self._unsupported(1.0)

        if reason_code is not None:
            return IntentRoute(REASON_INTENTS[reason_code], 1.0, True)

        matches: list[tuple[Intent, float]] = []
        for intent, signals in INTENT_SIGNALS.items():
            if any(signal in searchable for signal in signals):
                page_bonus = 0.1 if PAGE_INTENTS.get(page) is intent else 0.0
                matches.append((intent, min(1.0, 0.8 + page_bonus)))

        if len(matches) > 1:
            ranked = sorted(matches, key=lambda match: match[1], reverse=True)
            if ranked[0][1] - ranked[1][1] < 0.1:
                return self._unsupported(ranked[0][1])
            selected = ranked[0]
        elif matches:
            selected = matches[0]
        else:
            page_intent = PAGE_INTENTS.get(page)
            has_generic_help = any(signal in searchable for signal in GENERIC_HELP_SIGNALS)
            if page_intent is None or not has_generic_help:
                return self._unsupported(0.0)
            selected = (page_intent, 0.76)

        if selected[1] < self.confidence_threshold:
            return self._unsupported(selected[1])
        return IntentRoute(selected[0], selected[1], True)

    @staticmethod
    def _unsupported(confidence: float) -> IntentRoute:
        return IntentRoute(Intent.UNSUPPORTED, confidence, False)

