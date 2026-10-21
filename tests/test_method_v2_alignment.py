"""Tests for the 1.3 additions that carry specula-method 2.0 into the runtime."""
import json
from pathlib import Path

from specula_agent.orchestrator import ProjectState, SpeculaOrchestrator
from specula_agent.schemas import schema_filename_for, validate_artifact

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples" / "basic-case"


def _load(name):
    with (EXAMPLES / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def test_new_modes_route_to_new_schemas():
    assert schema_filename_for("4", "preferable_future") == "preferable_future.schema.json"
    for phase in ("4", "5", "6"):
        assert schema_filename_for(phase, "decision_log") == "decision_log.schema.json"
    assert schema_filename_for("4", "narrative_synthesis") == "phase4_narrative_system.schema.json"


def test_new_examples_validate_through_runtime_validator():
    assert validate_artifact(_load("preferable-future.json")) == []
    assert validate_artifact(_load("decision-log.json")) == []


def test_preferred_scenario_type_is_deprecated_but_still_valid():
    artifact = _load("phase-1-scenarios.json")
    artifact["payload"]["scenarios"][0]["scenario_type"] = "preferred"
    assert validate_artifact(artifact) == []


def test_unknown_archetype_is_rejected():
    artifact = _load("phase-1-scenarios.json")
    artifact["payload"]["scenarios"][0]["archetype"] = "utopia"
    assert validate_artifact(artifact)


def _orchestrator_after_guardian(report_overrides):
    state = ProjectState(project_id="project-test", current_phase="6")
    orchestrator = SpeculaOrchestrator(state)
    artifact = _load("phase-6-guardian.json")
    artifact["payload"]["guardian_report"].update(report_overrides)
    orchestrator._update_continuity_context(phase="6", artifact=artifact, validations=[])
    return state.continuity_context.get("decision_log", [])


def test_rupture_triggers_mandatory_re_speculation_alert():
    log = _orchestrator_after_guardian({"divergence_level": "rupture", "recommended_action": "correct"})
    assert any("GUARDIAN ALERT" in entry for entry in log)


def test_learning_drift_is_sent_to_the_circle():
    log = _orchestrator_after_guardian({"divergence_level": "drift", "recommended_action": "circle_deliberation"})
    assert any("GUARDIAN LEARNING" in entry for entry in log)
    assert not any("GUARDIAN ALERT" in entry for entry in log)
