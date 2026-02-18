"""Schema loading and artifact validation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator, FormatChecker

from .constants import ALLOWED_MODES, PHASE_SEQUENCE

SCHEMA_FILES: Dict[str, str] = {
    "0": "phase0_activation.schema.json",
    "1": "phase1_scenarios.schema.json",
    "1.5": "phase1_5_competitive_map.schema.json",
    "2": "phase2_brand_dna.schema.json",
    "3": "phase3_prototypes.schema.json",
    "4": "phase4_narrative_system.schema.json",
    "5": "phase5_cocreation.schema.json",
    "6": "phase6_guardian.schema.json",
}


class SchemaValidationError(ValueError):
    """Raised when an artifact fails schema or policy validation."""


def _schema_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas"


def _load_schema(filename: str) -> Dict[str, Any]:
    schema_path = _schema_dir() / filename
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def schema_filename_for(phase: str, mode: str) -> str:
    """Resolve schema file for a phase/mode pair."""
    if phase == "3" and mode == "refusal_register":
        return "phase3_refusals.schema.json"
    return SCHEMA_FILES[phase]


def validate_artifact(
    artifact: Dict[str, Any],
    current_phase: str | None = None,
) -> List[str]:
    """Validate artifact structure and canonical meta rules."""
    errors: List[str] = []
    meta = artifact.get("meta", {})
    phase = str(meta.get("phase", ""))
    mode = str(meta.get("mode", ""))

    if phase not in PHASE_SEQUENCE:
        errors.append(f"meta.phase must be one of {PHASE_SEQUENCE}; found `{phase}`")
        return errors

    if current_phase is not None and phase != str(current_phase):
        errors.append(f"meta.phase `{phase}` does not match current phase `{current_phase}`")

    if mode not in ALLOWED_MODES:
        errors.append(f"meta.mode `{mode}` is not in canonical mode enum")
        return errors

    schema_filename = schema_filename_for(phase, mode)
    schema = _load_schema(schema_filename)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors: List[Tuple[str, str]] = []

    for issue in validator.iter_errors(artifact):
        path = ".".join(str(item) for item in issue.path) or "$"
        schema_errors.append((path, issue.message))

    for path, message in sorted(schema_errors):
        errors.append(f"{path}: {message}")

    return errors


def assert_artifact_valid(artifact: Dict[str, Any], current_phase: str | None = None) -> None:
    """Raise with readable details when artifact is invalid."""
    errors = validate_artifact(artifact, current_phase=current_phase)
    if errors:
        raise SchemaValidationError("\n".join(errors))
