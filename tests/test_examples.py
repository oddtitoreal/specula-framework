"""Contract test: every basic-case example must validate against its phase schema.

This closes the gap where the runtime test-suite exercised the orchestrator but
never validated the shipped `examples/` against `schemas/`. See governance:
schemas are the declared "single source of truth", so examples are contracts too.
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples" / "basic-case"
SCHEMAS = REPO / "schemas"

# example filename -> schema filename
EXAMPLE_SCHEMA_MAP = {
    "phase-0-activation.json": "phase0_activation.schema.json",
    "phase-1-scenarios.json": "phase1_scenarios.schema.json",
    "phase-1.5-competitive-map.json": "phase1_5_competitive_map.schema.json",
    "phase-2-brand-dna.json": "phase2_brand_dna.schema.json",
    "phase-3-prototypes.json": "phase3_prototypes.schema.json",
    "phase-3-refusals.json": "phase3_refusals.schema.json",
    "phase-4-narrative.json": "phase4_narrative_system.schema.json",
    "phase-5-cocreation.json": "phase5_cocreation.schema.json",
    "phase-6-guardian.json": "phase6_guardian.schema.json",
}


def _load(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize("example_name,schema_name", sorted(EXAMPLE_SCHEMA_MAP.items()))
def test_example_validates_against_schema(example_name, schema_name):
    example_path = EXAMPLES / example_name
    schema_path = SCHEMAS / schema_name
    assert example_path.exists(), f"missing example: {example_path}"
    assert schema_path.exists(), f"missing schema: {schema_path}"

    validator = Draft202012Validator(_load(schema_path))
    errors = sorted(validator.iter_errors(_load(example_path)), key=lambda e: list(e.path))
    if errors:
        details = "\n".join(
            f"  - {'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in errors
        )
        pytest.fail(f"{example_name} fails {schema_name} ({len(errors)} errors):\n{details}")


def test_every_example_is_mapped():
    """Guard: a new example file without a schema mapping should fail loudly."""
    on_disk = {p.name for p in EXAMPLES.glob("*.json")}
    unmapped = on_disk - set(EXAMPLE_SCHEMA_MAP)
    assert not unmapped, f"examples without a schema mapping: {sorted(unmapped)}"
