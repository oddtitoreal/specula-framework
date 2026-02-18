import pytest

from specula_agent.constants import NEXT_PHASE
from specula_agent.llm import LLMProviderError
from specula_agent.orchestrator import ProjectState, SpeculaOrchestrator


def test_generate_step_updates_latest_artifact_for_current_phase():
    state = ProjectState(project_id="project-test", current_phase="1")
    orchestrator = SpeculaOrchestrator(state)
    result = orchestrator.generate_step(user_input="generate scenarios")

    artifact_id = result["artifact"]["meta"]["artifact_id"]
    assert state.latest_artifacts["1"] == artifact_id


def test_advance_requires_human_validation_true():
    state = ProjectState(project_id="project-test", current_phase="2")
    orchestrator = SpeculaOrchestrator(state)

    with pytest.raises(ValueError):
        orchestrator.advance_after_validation(
            phase="2",
            artifact_id="artifact-123",
            validated_by_human=False,
        )


def test_advance_moves_to_next_phase():
    state = ProjectState(project_id="project-test", current_phase="3")
    orchestrator = SpeculaOrchestrator(state)

    next_phase = orchestrator.advance_after_validation(
        phase="3",
        artifact_id="artifact-123",
        validated_by_human=True,
    )

    assert next_phase == NEXT_PHASE["3"]
    assert state.current_phase == "4"
    assert state.latest_artifacts["3"] == "artifact-123"


def test_advance_fails_if_phase_does_not_match_state():
    state = ProjectState(project_id="project-test", current_phase="4")
    orchestrator = SpeculaOrchestrator(state)

    with pytest.raises(ValueError):
        orchestrator.advance_after_validation(
            phase="3",
            artifact_id="artifact-123",
            validated_by_human=True,
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
    orchestrator = SpeculaOrchestrator(state, llm_client=_ValidLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert "Which scenario should we validate first?" in result["assistant_text"]


def test_orchestrator_falls_back_when_llm_output_is_invalid():
    state = ProjectState(project_id="project-test", current_phase="1")
    orchestrator = SpeculaOrchestrator(state, llm_client=_InvalidLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert "Which scenario should we validate first as the exploration anchor?" in result["assistant_text"]


def test_orchestrator_falls_back_when_llm_fails():
    state = ProjectState(project_id="project-test", current_phase="1")
    orchestrator = SpeculaOrchestrator(state, llm_client=_FailingLLM())
    result = orchestrator.generate_step(user_input="generate scenarios")
    assert result["assistant_text"].startswith("MODE: exploration | PHASE: 1")
