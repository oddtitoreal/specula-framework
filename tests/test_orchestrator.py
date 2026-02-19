import pytest

from specula_agent.constants import NEXT_PHASE, PHASE_SEQUENCE
from specula_agent.llm import LLMProviderError
from specula_agent.orchestrator import ProjectState, SpeculaOrchestrator


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


def test_generate_step_updates_latest_artifact_for_current_phase():
    state = ProjectState(project_id="project-test", current_phase="1")
    _seed_prerequisites(state, "1")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="generate scenarios")

    artifact_id = result["artifact"]["meta"]["artifact_id"]
    assert state.latest_artifacts["1"] == artifact_id


def test_generate_step_blocks_when_prerequisites_are_missing():
    state = ProjectState(project_id="project-test", current_phase="4")
    orchestrator = SpeculaOrchestrator(state)

    with pytest.raises(ValueError, match="validated prerequisite phases"):
        orchestrator.generate_step(user_input="synthesize narrative")


def test_advance_requires_two_human_approvals():
    state = ProjectState(project_id="project-test", current_phase="2")
    _seed_prerequisites(state, "2")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="define dna", phase="2")
    artifact_id = result["artifact"]["meta"]["artifact_id"]

    with pytest.raises(ValueError, match="at least two human approvals"):
        orchestrator.advance_after_validation(
            phase="2",
            artifact_id=artifact_id,
            validations=[
                {
                    "validator_id": "v1",
                    "validator_role": "strategy_lead",
                    "decision": "approve",
                    "validated_by_human": True,
                }
            ],
        )


def test_advance_requires_distinct_reviewer_roles():
    state = ProjectState(project_id="project-test", current_phase="3")
    _seed_prerequisites(state, "3")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="prototype", phase="3")
    artifact_id = result["artifact"]["meta"]["artifact_id"]

    with pytest.raises(ValueError, match="distinct validator roles"):
        orchestrator.advance_after_validation(
            phase="3",
            artifact_id=artifact_id,
            validations=[
                {
                    "validator_id": "v1",
                    "validator_role": "ethics_reviewer",
                    "decision": "approve",
                    "validated_by_human": True,
                },
                {
                    "validator_id": "v2",
                    "validator_role": "ethics_reviewer",
                    "decision": "approve",
                    "validated_by_human": True,
                },
            ],
        )


def test_state_rejects_duplicate_validator_signature():
    state = ProjectState(project_id="project-test", current_phase="0")
    state.add_validation_record(
        artifact_id="artifact-1",
        validator_id="reviewer-1",
        validator_role="strategy_lead",
        decision="approve",
        validated_by_human=True,
    )
    with pytest.raises(ValueError, match="duplicate validator signature"):
        state.add_validation_record(
            artifact_id="artifact-1",
            validator_id="reviewer-1",
            validator_role="ethics_reviewer",
            decision="approve",
            validated_by_human=True,
        )


def test_advance_moves_to_next_phase():
    state = ProjectState(project_id="project-test", current_phase="3")
    _seed_prerequisites(state, "3")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="prototype", phase="3")
    artifact_id = result["artifact"]["meta"]["artifact_id"]

    next_phase = orchestrator.advance_after_validation(
        phase="3",
        artifact_id=artifact_id,
        validations=[
            {
                "validator_id": "v1",
                "validator_role": "ethics_reviewer",
                "decision": "approve",
                "validated_by_human": True,
            },
            {
                "validator_id": "v2",
                "validator_role": "brand_lead",
                "decision": "approve",
                "validated_by_human": True,
            },
        ],
    )

    assert next_phase == NEXT_PHASE["3"]
    assert state.current_phase == "4"
    assert state.latest_artifacts["3"] == artifact_id
    assert state.phase_validated_artifacts["3"] == artifact_id


def test_advance_fails_if_phase_does_not_match_state():
    state = ProjectState(project_id="project-test", current_phase="4")
    _seed_prerequisites(state, "4")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="narrative", phase="4")
    artifact_id = result["artifact"]["meta"]["artifact_id"]

    with pytest.raises(ValueError):
        orchestrator.advance_after_validation(
            phase="3",
            artifact_id=artifact_id,
            validations=[
                {
                    "validator_id": "v1",
                    "validator_role": "strategy_lead",
                    "decision": "approve",
                    "validated_by_human": True,
                },
                {
                    "validator_id": "v2",
                    "validator_role": "ethics_reviewer",
                    "decision": "approve",
                    "validated_by_human": True,
                },
            ],
        )


class _ValidLLM:
    def generate_assistant_text(self, **kwargs):
        return (
            "MODE: exploration | PHASE: 1\n"
            "I prepared a scenario divergence seed.\n"
            "Which scenario should we validate first?"
        )


class _InvalidLLM:
    def generate_assistant_text(self, **kwargs):
        return "MODE: exploration | PHASE: 1\nYou should choose this.\nWhy?\nAnd why?"


class _FailingLLM:
    def generate_assistant_text(self, **kwargs):
        raise LLMProviderError("provider unavailable")


def test_orchestrator_uses_valid_llm_output():
    state = ProjectState(project_id="project-test", current_phase="1")
    _seed_prerequisites(state, "1")
    orchestrator = SpeculaOrchestrator(state, llm_client=_ValidLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert "Which scenario should we validate first?" in result["assistant_text"]


def test_orchestrator_falls_back_when_llm_output_is_invalid():
    state = ProjectState(project_id="project-test", current_phase="1")
    _seed_prerequisites(state, "1")
    orchestrator = SpeculaOrchestrator(state, llm_client=_InvalidLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert "Which scenario should we validate first as the exploration anchor?" in result["assistant_text"]


def test_orchestrator_falls_back_when_llm_fails():
    state = ProjectState(project_id="project-test", current_phase="1")
    _seed_prerequisites(state, "1")
    orchestrator = SpeculaOrchestrator(state, llm_client=_FailingLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert result["assistant_text"].startswith("MODE: exploration | PHASE: 1")
