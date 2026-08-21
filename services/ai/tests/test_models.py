import pytest
from pydantic import ValidationError

from app.models import (
    CanonicalAssistantRequest,
    DLPResult,
    EvidenceChunk,
    EvidencePacket,
    ProviderResult,
)
from app.models.enums import DLPAction, Intent, Locale, Page, ReasonCode, Service


def test_internal_trust_boundary_models_are_strict() -> None:
    canonical = CanonicalAssistantRequest(
        intent=Intent.NO_APPOINTMENT_AVAILABLE,
        locale=Locale.ENGLISH,
        service=Service.DRIVING_LICENCE,
        page=Page.APPOINTMENT_WAITLIST,
        reasonCode=ReasonCode.NO_MATCHING_SLOT,
    )
    dlp = DLPResult(action=DLPAction.ALLOW, entityTypes=[], intent=canonical.intent)
    evidence = EvidencePacket(
        intent=canonical.intent,
        chunks=[
            EvidenceChunk(
                sourceId="synthetic-public-source",
                title="Synthetic public guidance",
                content="No matching appointment is available.",
                jurisdiction="Delhi",
            )
        ],
    )
    result = ProviderResult(
        answer="No matching appointment is available.",
        sourceIds=["synthetic-public-source"],
        uncertain=False,
        escalation=None,
    )

    assert "question" not in canonical.model_dump()
    assert dlp.action is DLPAction.ALLOW
    assert len(evidence.chunks) == 1
    assert result.source_ids == ["synthetic-public-source"]

    with pytest.raises(ValidationError):
        CanonicalAssistantRequest(
            intent=Intent.CURRENT_STEP,
            locale=Locale.ENGLISH,
            service=Service.DRIVING_LICENCE,
            page=Page.DASHBOARD,
            raw_question="this field must never exist",
        )


def test_evidence_packet_is_bounded() -> None:
    chunks = [
        EvidenceChunk(
            sourceId=f"source-{index}",
            title="Synthetic public guidance",
            content="Synthetic content",
            jurisdiction="Delhi",
        )
        for index in range(5)
    ]

    with pytest.raises(ValidationError):
        EvidencePacket(intent=Intent.CURRENT_STEP, chunks=chunks)

