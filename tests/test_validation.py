from specula_agent.orchestrator import ProjectState, SpeculaOrchestrator
from specula_agent.policy import validate_assistant_text
from specula_agent.schemas import validate_artifact
from specula_agent.constants import PHASE_SEQUENCE


def _seed_prerequisites(state: ProjectState, phase: str) -> None:
    index = PHASE_SEQUENCE.index(phase)
    for prereq in PHASE_SEQUENCE[:index]:
        artifact_id = f"validated-{prereq}"
        state.phase_validated_artifacts[prereq] = artifact_id
        state.latest_artifacts[prereq] = artifact_id
        state.artifact_index[artifact_id] = {
            "meta": {"artifact_id": artifact_id, "phase": prereq, "mode": "sensemaking"},
            "payload": {},
        }


def _make_artifact(phase: str):
    state = ProjectState(project_id="project-test", current_phase=phase)
    _seed_prerequisites(state, phase)
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="test input", phase=phase)
    return result["artifact"], result["assistant_text"]


def test_schema_validation_passes_for_all_default_phases():
    for phase in ("0", "1", "1.5", "2", "3", "4", "5", "6"):
        artifact, _ = _make_artifact(phase)
        assert validate_artifact(artifact, current_phase=phase) == []


def test_schema_validation_passes_for_phase3_refusal_mode():
    state = ProjectState(project_id="project-test", current_phase="3")
    _seed_prerequisites(state, "3")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(
        user_input="log a refusal",
        phase="3",
        mode="refusal_register",
    )
    assert validate_artifact(result["artifact"], current_phase="3") == []


def test_phase_consistency_fails_on_mismatch():
    artifact, _ = _make_artifact("1")
    errors = validate_artifact(artifact, current_phase="2")
    assert any("does not match current phase" in error for error in errors)


def test_mode_enum_fails_for_unknown_mode():
    artifact, _ = _make_artifact("2")
    artifact["meta"]["mode"] = "unknown_mode"
    errors = validate_artifact(artifact, current_phase="2")
    assert any("canonical mode enum" in error for error in errors)


def test_human_validation_default_false_is_enforced():
    artifact, _ = _make_artifact("4")
    artifact["meta"]["validated_by_human"] = True
    errors = validate_artifact(artifact, current_phase="4")
    assert any("False was expected" in error for error in errors)


def test_assistant_text_validation_passes_for_generated_output():
    _, assistant_text = _make_artifact("5")
    assert validate_assistant_text(assistant_text) == []


def test_one_question_rule_fails_when_multiple_questions():
    invalid = "MODE: sensemaking | PHASE: 0\nLine\nQuestion one?\nQuestion two?"
    errors = validate_assistant_text(invalid)
    assert any("exactly one question mark" in error for error in errors)


def test_header_rule_fails_for_invalid_header():
    invalid = "mode=sensemaking phase=0\nLine\nWhat is the validator role?"
    errors = validate_assistant_text(invalid)
    assert any("first line must match" in error for error in errors)


def test_six_line_limit_before_question_is_enforced():
    invalid = "\n".join(
        [
            "MODE: sensemaking | PHASE: 0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "What is the validator role?",
        ]
    )
    errors = validate_assistant_text(invalid)
    assert any("more than 6 lines" in error for error in errors)
