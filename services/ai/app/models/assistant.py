"""Pydantic contracts for safe assistant processing."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.models.enums import (
    BlockedReason,
    DLPAction,
    Intent,
    Locale,
    Page,
    PIIEntityType,
    ReasonCode,
    Service,
)

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
QuestionText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=500),
]


class StrictModel(BaseModel):
    """Reject fields that were not explicitly approved for a trust boundary."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class AssistantRequest(StrictModel):
    question: QuestionText
    locale: Locale
    service: Service
    page: Page
    reason_code: ReasonCode | None = Field(default=None, alias="reasonCode")

class AssistantResponse(StrictModel):
    answer: NonEmptyText
    source_ids: list[str] = Field(default_factory=list, alias="sourceIds")
    uncertain: bool
    escalation: str | None = None
    fallback_used: bool = Field(alias="fallbackUsed")
    blocked_reason: BlockedReason | None = Field(default=None, alias="blockedReason")


class DLPResult(StrictModel):
    action: DLPAction
    entity_types: list[PIIEntityType] = Field(default_factory=list, alias="entityTypes")
    intent: Intent | None = None


class CanonicalAssistantRequest(StrictModel):
    """Provider-safe request that deliberately has no raw-question field."""

    intent: Intent
    locale: Locale
    service: Service
    page: Page
    reason_code: ReasonCode | None = Field(default=None, alias="reasonCode")


class EvidenceChunk(StrictModel):
    source_id: NonEmptyText = Field(alias="sourceId")
    title: NonEmptyText
    content: NonEmptyText
    jurisdiction: NonEmptyText


class EvidencePacket(StrictModel):
    intent: Intent
    chunks: list[EvidenceChunk] = Field(default_factory=list, max_length=4)


class ProviderResult(StrictModel):
    answer: NonEmptyText
    source_ids: list[str] = Field(default_factory=list, alias="sourceIds")
    uncertain: bool
    escalation: str | None = None
