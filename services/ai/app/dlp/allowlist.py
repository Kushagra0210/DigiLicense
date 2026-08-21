"""Narrow allowlist for obvious documentation placeholders, never real identifiers."""

import re

SEPARATORS = re.compile(r"[\s:_-]+")
SAFE_EXACT_EXAMPLES = {
    "abcde1234f",
    "example@upi",
    "sample@upi",
    "dummy@upi",
}


def is_safe_placeholder(candidate: str) -> bool:
    compact = SEPARATORS.sub("", candidate).casefold()
    if compact in SAFE_EXACT_EXAMPLES:
        return True
    return bool(compact and set(compact) <= {"x", "*", "0"})
