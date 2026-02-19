from specula_agent.orchestrator import ProjectState
from specula_agent.storage import build_storage


def test_noop_storage_adapter_methods_are_safe():
    storage = build_storage(None)
    state = ProjectState(project_id="project-test", current_phase="0")

    storage.init_schema()
    storage.upsert_project_state(state)
    storage.insert_artifact(
        state.project_id,
        {
            "meta": {
                "artifact_id": "artifact-1",
                "phase": "0",
                "mode": "sensemaking",
                "generated_at": "2026-02-18T00:00:00Z",
                "validated_by_human": False,
                "related_artifacts": [],
            },
            "payload": {
                "activation_status": "active",
                "current_phase": 0,
                "context_set": True,
                "next_required_input": "decision_authority",
            },
        },
    )
    storage.insert_validation(
        "artifact-1",
        validated_by_human=True,
        validator_id="validator",
        validator_role="strategy_lead",
        decision="approve",
    )
    storage.insert_validation(
        "artifact-1",
        validated_by_human=True,
        validator_id="validator-2",
        validator_role="ethics_reviewer",
        decision="approve",
    )
    assert storage.get_validations("artifact-1") == []
    storage.append_audit(
        project_id=state.project_id,
        phase="0",
        mode="sensemaking",
        event="TEST_EVENT",
        content="ok",
    )
