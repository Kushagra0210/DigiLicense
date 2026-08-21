"""Security-oriented text normalization performed before PII detection."""

import re
import unicodedata
from dataclasses import dataclass, field

DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True, slots=True)
class NormalizedText:
    """Text safe for deterministic analysis, but still sensitive and never loggable."""

    value: str = field(repr=False)

    def __str__(self) -> str:
        # Prevent accidental interpolation into logs and exception messages.
        return "[NORMALIZED_TEXT_REDACTED]"

    def __repr__(self) -> str:
        return "NormalizedText([REDACTED])"


def normalize_for_analysis(text: str) -> NormalizedText:
    """Normalize common Unicode and obfuscation tricks without preserving hidden characters."""

    normalized = unicodedata.normalize("NFKC", text).translate(DEVANAGARI_DIGITS)
    visible_characters: list[str] = []

    for character in normalized:
        category = unicodedata.category(character)
        if category == "Cf":
            # Format controls include zero-width joiners/non-joiners and directional marks.
            continue
        if category.startswith("C") and character not in {"\n", "\r", "\t"}:
            visible_characters.append(" ")
            continue
        visible_characters.append(character)

    collapsed = WHITESPACE.sub(" ", "".join(visible_characters)).strip()
    return NormalizedText(collapsed)
