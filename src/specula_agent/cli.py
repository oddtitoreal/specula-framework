"""Command line interface for the Specula runtime MVP."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from .llm import LLMClient
from .orchestrator import ProjectState, SpeculaOrchestrator
from .policy import validate_assistant_text
from .schemas import validate_artifact
from .storage import StorageError, build_storage


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def _load_state(path: Path) -> ProjectState:
    if path.exists():
        return ProjectState.from_dict(_load_json(path))
    return ProjectState(project_id=f"project-{uuid4()}", current_phase="0")


def _cmd_step(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    state = _load_state(state_path)
    storage = build_storage(args.database_url)
    storage.init_schema()

    llm_client = None
    if args.llm_provider:
        llm_client = LLMClient.from_env(
            provider=args.llm_provider,
            model=args.llm_model,
            api_key_env=args.llm_api_key_env,
            base_url=args.llm_base_url,
            base_prompt_file=args.base_prompt_file,
        )

    orchestrator = SpeculaOrchestrator(state, llm_client=llm_client)

    result = orchestrator.generate_step(
        user_input=args.user_input,
        phase=args.phase,
        mode=args.mode,
    )

    _save_json(state_path, state.to_dict())

    response = {
        "assistant_text": result["assistant_text"],
        "artifact": result["artifact"],
        "state": state.to_dict(),
    }

    if args.output_file:
        _save_json(Path(args.output_file), response)

    storage.upsert_project_state(state)
    storage.insert_artifact(state.project_id, result["artifact"])
    storage.append_audit(
        project_id=state.project_id,
        phase=result["artifact"]["meta"]["phase"],
        mode=result["artifact"]["meta"]["mode"],
        event="STEP_GENERATED",
        content=result["assistant_text"],
    )

    print(result["assistant_text"])
    print(json.dumps(result["artifact"], indent=2))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    artifact = _load_json(Path(args.artifact_file))
    with Path(args.text_file).open("r", encoding="utf-8") as handle:
        assistant_text = handle.read()
    storage = build_storage(args.database_url)
    storage.init_schema()

    errors = []
    errors.extend(validate_assistant_text(assistant_text))
    errors.extend(validate_artifact(artifact, current_phase=args.current_phase))

    if errors:
        storage.append_audit(
            project_id=args.project_id,
            phase=artifact.get("meta", {}).get("phase"),
            mode=artifact.get("meta", {}).get("mode"),
            event="VALIDATION_FAILED",
            content="; ".join(errors),
        )
        print("validation failed:")
        for issue in errors:
            print(f"- {issue}")
        return 1

    storage.append_audit(
        project_id=args.project_id,
        phase=artifact.get("meta", {}).get("phase"),
        mode=artifact.get("meta", {}).get("mode"),
        event="VALIDATION_PASSED",
        content="assistant text + artifact contract valid",
    )
    print("validation passed")
    return 0


def _cmd_advance(args: argparse.Namespace) -> int:
    state_path = Path(args.state_file)
    state = _load_state(state_path)
    storage = build_storage(args.database_url)
    storage.init_schema()
    if args.decision == "approve" and not args.validated_by_human:
        raise ValueError("approve decision requires --validated-by-human")

    state.add_validation_record(
        artifact_id=args.artifact_id,
        validator_id=args.validator_id,
        validator_role=args.validator_role,
        decision=args.decision,
        validated_by_human=args.validated_by_human,
    )

    storage.insert_validation(
        args.artifact_id,
        validated_by_human=args.validated_by_human,
        validator_id=args.validator_id,
        validator_role=args.validator_role,
        decision=args.decision,
    )

    _save_json(state_path, state.to_dict())
    storage.upsert_project_state(state)
    storage.append_audit(
        project_id=state.project_id,
        phase=args.phase,
        mode=None,
        event="VALIDATION_RECORDED",
        content=(
            f"validator={args.validator_id}; role={args.validator_role}; "
            f"decision={args.decision}; human={args.validated_by_human}"
        ),
    )

    orchestrator = SpeculaOrchestrator(state)
    validations = state.validation_snapshot(args.artifact_id)
    next_phase = orchestrator.advance_after_validation(phase=args.phase, artifact_id=args.artifact_id, validations=validations)

    _save_json(state_path, state.to_dict())
    storage.upsert_project_state(state)
    storage.append_audit(
        project_id=state.project_id,
        phase=args.phase,
        mode=None,
        event="PHASE_ADVANCED",
        content=f"advanced to phase {next_phase}",
    )
    print(f"advanced to phase {next_phase}")
    return 0


def _cmd_init_db(args: argparse.Namespace) -> int:
    storage = build_storage(args.database_url)
    storage.init_schema()
    print("database schema initialized")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Specula runtime MVP CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    step = subparsers.add_parser("step", help="Generate one validated agent step")
    step.add_argument("--state-file", default=".specula_state.json")
    step.add_argument("--user-input", required=True)
    step.add_argument("--phase")
    step.add_argument("--mode")
    step.add_argument("--output-file")
    step.add_argument("--database-url", default=os.getenv("SPECULA_DATABASE_URL"))
    step.add_argument("--llm-provider", choices=["openai", "anthropic"])
    step.add_argument("--llm-model", default="gpt-4o-mini")
    step.add_argument("--llm-api-key-env", default="OPENAI_API_KEY")
    step.add_argument("--llm-base-url")
    step.add_argument(
        "--base-prompt-file",
        default="prompts/specula_method_agent_base.md",
    )
    step.set_defaults(func=_cmd_step)

    validate = subparsers.add_parser("validate", help="Validate assistant text + artifact")
    validate.add_argument("--artifact-file", required=True)
    validate.add_argument("--text-file", required=True)
    validate.add_argument("--current-phase")
    validate.add_argument("--database-url", default=os.getenv("SPECULA_DATABASE_URL"))
    validate.add_argument("--project-id", default="project-validation")
    validate.set_defaults(func=_cmd_validate)

    advance = subparsers.add_parser("advance", help="Advance state after human validation")
    advance.add_argument("--state-file", default=".specula_state.json")
    advance.add_argument("--phase", required=True)
    advance.add_argument("--artifact-id", required=True)
    advance.add_argument(
        "--validated-by-human",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    advance.add_argument("--validator-id", default="human-validator")
    advance.add_argument("--validator-role", required=True)
    advance.add_argument("--decision", choices=["approve", "reject", "hold"], default="approve")
    advance.add_argument("--database-url", default=os.getenv("SPECULA_DATABASE_URL"))
    advance.set_defaults(func=_cmd_advance)

    init_db = subparsers.add_parser("init-db", help="Initialize PostgreSQL schema")
    init_db.add_argument("--database-url", default=os.getenv("SPECULA_DATABASE_URL"))
    init_db.set_defaults(func=_cmd_init_db)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init-db" and not getattr(args, "database_url", None):
            raise StorageError("database URL is required for init-db")
        return args.func(args)
    except Exception as exc:  # pragma: no cover
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
