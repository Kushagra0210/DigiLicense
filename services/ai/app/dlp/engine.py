"""Presidio-backed DLP engine which returns classifications, never detected values."""

from dataclasses import dataclass

from app.dlp.allowlist import is_safe_placeholder
from app.dlp.recognizers import RecognizerPolicy, india_recognizer_policies
from app.models import DLPResult
from app.models.enums import DLPAction, PIIEntityType
from app.normalization import NormalizedText, normalize_for_analysis


@dataclass(frozen=True, slots=True)
class DLPInspection:
    normalized_text: NormalizedText
    result: DLPResult


class PresidioDLPService:
    """Run an explicit, deterministic Presidio pattern-recognizer registry."""

    def __init__(
        self,
        score_threshold: float = 0.45,
        policies: tuple[RecognizerPolicy, ...] | None = None,
    ) -> None:
        self.score_threshold = score_threshold
        self.policies = policies or india_recognizer_policies()

    @property
    def enabled_recognizer_names(self) -> tuple[str, ...]:
        return tuple(policy.recognizer.name for policy in self.policies)

    def inspect(self, text: str) -> DLPInspection:
        normalized = normalize_for_analysis(text)
        detected: set[PIIEntityType] = set()
        searchable_text = normalized.value
        casefolded_text = searchable_text.casefold()

        for policy in self.policies:
            context_present = any(
                context.casefold() in casefolded_text for context in policy.contexts
            )
            if policy.context_required and not context_present:
                continue

            results = policy.recognizer.analyze(
                text=searchable_text,
                entities=policy.recognizer.supported_entities,
                nlp_artifacts=None,
            )
            for result in results:
                candidate = searchable_text[result.start : result.end]
                if is_safe_placeholder(candidate):
                    continue
                contextual_score = min(1.0, result.score + (0.35 if context_present else 0.0))
                threshold = max(self.score_threshold, policy.minimum_score)
                if contextual_score >= threshold:
                    detected.add(policy.entity_type)

        action = DLPAction.BLOCK_PII if detected else DLPAction.ALLOW
        return DLPInspection(
            normalized_text=normalized,
            result=DLPResult(
                action=action,
                entityTypes=sorted(detected, key=lambda entity: entity.value),
                intent=None,
            ),
        )
