"""Validation rules for assistant text behavior."""

from __future__ import annotations

import re
from typing import List

from .constants import FORBIDDEN_PHRASES

HEADER_RE = re.compile(r"^MODE:\s+([a-z_]+)\s+\|\s+PHASE:\s+(0|1|1\.5|2|3|4|5|6)$")


def validate_assistant_text(text: str) -> List[str]:
    """Validate non-oracular and formatting constraints for assistant output."""
    errors: List[str] = []
    if not text or not text.strip():
        return ["assistant text is empty"]

    lines = text.strip().splitlines()
    if not HEADER_RE.match(lines[0].strip()):
        errors.append("first line must match `MODE: <mode> | PHASE: <phase>`")

    question_count = text.count("?")
    if question_count != 1:
        errors.append(f"assistant text must contain exactly one question mark; found {question_count}")

    question_line_idx = next((idx for idx, line in enumerate(lines) if "?" in line), None)
    if question_line_idx is None:
        errors.append("assistant text must include one explicit question line")
    else:
        if question_line_idx > 6:
            errors.append("assistant text has more than 6 lines before the question line")

    lowered = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            errors.append(f"forbidden prescriptive phrase detected: `{phrase}`")

    if "decision: true" in lowered or "decision=true" in lowered:
        errors.append("forbidden decision field detected in assistant text")

    return errors
