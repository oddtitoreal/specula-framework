"""Executable orchestrator for Specula agent sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from .constants import NEXT_PHASE, PHASE_DEFAULT_MODE, PHASE_SEQUENCE
from .llm import LLMClient, LLMProviderError
from .policy import validate_assistant_text
from .schemas import assert_artifact_valid

VALIDATION_DECISIONS = {"approve", "reject", "hold"}
PHASE_PREREQUISITES = {
    "0": (),
    "1": ("0",),
    "1.5": ("1",),
    "2": ("1", "1.5"),
    "3": ("2",),
    "4": ("2", "3"),
    "5": ("4",),
    "6": ("5",),
}
PHASE_ORDER = {phase: idx for idx, phase in enumerate(PHASE_SEQUENCE)}


def _default_continuity_context() -> Dict[str, List[str]]:
    return {
        "decision_log": [],
        "radical_values": [],
        "refusal_signals": [],
        "open_assumptions": [],
    }


def _normalize_str_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    result: List[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


def _phase_sort_key(phase: str) -> int:
    return PHASE_ORDER.get(str(phase), 999)


@dataclass
class ProjectState:
    """In-memory state used by the orchestrator."""

    project_id: str
    current_phase: str = "0"
    latest_artifacts: Dict[str, str] = field(default_factory=dict)
    phase_validated_artifacts: Dict[str, str] = field(default_factory=dict)
    artifact_index: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    validation_records: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    continuity_context: Dict[str, List[str]] = field(default_factory=_default_continuity_context)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectState":
        continuity = _default_continuity_context()
        raw_continuity = data.get("continuity_context", {})
        if isinstance(raw_continuity, dict):
            for key in continuity:
                continuity[key] = _normalize_str_list(raw_continuity.get(key, []))

        raw_validation_records = data.get("validation_records", {})
        validation_records: Dict[str, List[Dict[str, Any]]] = {}
        if isinstance(raw_validation_records, dict):
            for artifact_id, rows in raw_validation_records.items():
                if not isinstance(rows, list):
                    continue
                clean_rows: List[Dict[str, Any]] = []
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    validator_id = str(row.get("validator_id", "")).strip()
                    validator_role = str(row.get("validator_role", "")).strip()
                    decision = str(row.get("decision", "hold")).lower().strip()
                    if not validator_id or not validator_role or decision not in VALIDATION_DECISIONS:
                        continue
                    clean_rows.append(
                        {
                            "validator_id": validator_id,
                            "validator_role": validator_role,
                            "decision": decision,
                            "validated_by_human": bool(row.get("validated_by_human", False)),
                            "validated_at": str(row.get("validated_at") or _now_iso()),
                        }
                    )
                validation_records[str(artifact_id)] = clean_rows

        return cls(
            project_id=data["project_id"],
            current_phase=str(data.get("current_phase", "0")),
            latest_artifacts=dict(data.get("latest_artifacts", {})),
            phase_validated_artifacts=dict(data.get("phase_validated_artifacts", {})),
            artifact_index=dict(data.get("artifact_index", {})),
            validation_records=validation_records,
            continuity_context=continuity,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "current_phase": self.current_phase,
            "latest_artifacts": self.latest_artifacts,
            "phase_validated_artifacts": self.phase_validated_artifacts,
            "artifact_index": self.artifact_index,
            "validation_records": self.validation_records,
            "continuity_context": self.continuity_context,
        }

    def add_validation_record(
        self,
        *,
        artifact_id: str,
        validator_id: str,
        validator_role: str,
        decision: str,
        validated_by_human: bool,
    ) -> None:
        artifact_key = str(artifact_id)
        validator_key = str(validator_id).strip()
        role_key = str(validator_role).strip()
        decision_key = str(decision).lower().strip()
        if not validator_key:
            raise ValueError("validator_id cannot be empty")
        if not role_key:
            raise ValueError("validator_role cannot be empty")
        if decision_key not in VALIDATION_DECISIONS:
            raise ValueError(f"decision must be one of {sorted(VALIDATION_DECISIONS)}")

        rows = self.validation_records.setdefault(artifact_key, [])
        if any(row.get("validator_id") == validator_key for row in rows):
            raise ValueError(
                f"duplicate validator signature is not allowed for `{artifact_key}` and `{validator_key}`"
            )

        rows.append(
            {
                "validator_id": validator_key,
                "validator_role": role_key,
                "decision": decision_key,
                "validated_by_human": bool(validated_by_human),
                "validated_at": _now_iso(),
            }
        )

    def validation_snapshot(self, artifact_id: str) -> List[Dict[str, Any]]:
        return list(self.validation_records.get(str(artifact_id), []))


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _question_for_phase(phase: str) -> str:
    questions = {
        "0": "Who will validate phase outputs as the explicit human decision authority?",
        "1": "Which scenario should we validate first as the exploration anchor?",
        "1.5": "Which white space should we stress test before proceeding to archaeology?",
        "2": "Which radical value remains non-negotiable even if it increases short-term cost?",
        "3": "Which value boundary should we test against this prototype first?",
        "4": "Which storyline is most fragile when checked against your validated DNA?",
        "5": "Which divergence should remain open instead of being resolved now?",
        "6": "Which drift signal should trigger a re-speculation cycle immediately?",
    }
    return questions[phase]


def _framing_for_phase(phase: str) -> str:
    framings = {
        "0": "Project context is initialized and phase entry is active.",
        "1": "I generated a first divergence seed to open alternatives.",
        "1.5": "I mapped an initial competitive-futures hypothesis.",
        "2": "I drafted a first DNA structure from the available evidence.",
        "3": "I prepared a prototype draft with an explicit ethical check.",
        "4": "I assembled a first narrative system draft for stress testing.",
        "5": "I structured consensus and divergence signals from community input.",
        "6": "I compared current signals against scenarios and identity constraints.",
    }
    return framings[phase]


def build_payload_template(phase: str, mode: str) -> Dict[str, Any]:
    """Return a schema-valid payload skeleton for the selected phase."""
    if phase == "0":
        return {
            "activation_status": "active",
            "current_phase": 0,
            "context_set": True,
            "next_required_input": "decision_authority",
        }
    if phase == "1":
        return {
            "scenarios": [
                {
                    "scenario_id": f"scenario-{uuid4()}",
                    "name": "Scenario Seed",
                    "time_horizon": "10",
                    "drivers": [
                        {
                            "type": "cultural",
                            "description": "A relevant weak signal emerging in the target market",
                        }
                    ],
                    "scenario_type": "preferred",
                    "description": "A plausible but tension-rich future context.",
                    "maieutic_question": "What identity cost are we willing to accept in this scenario?",
                    "user_response": None,
                }
            ]
        }
    if phase == "1.5":
        return {
            "competitive_map": [
                {
                    "competitor": "Competitor A",
                    "future_trajectory": "Narrative ownership of a future category claim",
                    "occupied_territory": "High-visibility sustainability positioning",
                    "ignored_territories": ["Long-term trust infrastructure"],
                    "confidence_level": "medium",
                }
            ],
            "white_spaces": [
                {
                    "white_space_id": f"white-space-{uuid4()}",
                    "description": "Unoccupied identity territory with strategic relevance",
                    "strategic_risk": "medium",
                    "alignment_with_brand": "high",
                }
            ],
        }
    if phase == "2":
        return {
            "brand_dna": {
                "radical_values": [
                    {
                        "value": "value_name",
                        "tested_in": "decision context",
                        "cost_paid": "explicit trade-off",
                    }
                ],
                "accepted_biases": ["bias_name"],
                "moral_entity": "caretaker",
                "refusal_zones": ["non-negotiable exclusion"],
                "tensions": {
                    "acceptable": ["productive tension"],
                    "unacceptable": ["identity-breaking tension"],
                },
            }
        }
    if phase == "3" and mode == "refusal_register":
        return {
            "refusals": [
                {
                    "refusal_id": f"refusal-{uuid4()}",
                    "prototype_id": f"prototype-{uuid4()}",
                    "violated_value": "radical_value_name",
                    "opportunity_cost": "What we gave up by refusing this direction",
                    "identity_signal": "Boundary reinforced by this refusal",
                    "date": _now_iso(),
                    "ethical_gate_assessment": {
                        "question_1_value_violation_rationale": "Pending final rationale after review.",
                        "question_2_harmful_practice_rationale": "Pending final rationale after review.",
                        "question_3_unacceptable_dependency_rationale": "Pending final rationale after review.",
                        "reviewer_decision_refs": [
                            {
                                "validator_role": "pending_review",
                                "decision": "hold",
                                "reference": "Awaiting at least two human approvals.",
                            }
                        ],
                    },
                }
            ]
        }
    if phase == "3":
        return {
            "prototypes": [
                {
                    "prototype_id": f"prototype-{uuid4()}",
                    "scenario_id": f"scenario-{uuid4()}",
                    "description": "Prototype concept statement",
                    "role_in_future": "Defined role in the target scenario",
                    "stakeholder_impact": {
                        "winners": ["stakeholder_group"],
                        "losers": ["stakeholder_group"],
                    },
                    "ethical_gate": {
                        "status": "HOLD",
                        "violated_values": [],
                        "systemic_impact": "aligned",
                        "question_1_value_violation_rationale": "Pending explicit value-violation assessment.",
                        "question_2_harmful_practice_rationale": "Pending explicit harmful-practice assessment.",
                        "question_3_unacceptable_dependency_rationale": "Pending explicit dependency assessment.",
                        "reviewer_decision_refs": [
                            {
                                "validator_role": "pending_review",
                                "decision": "hold",
                                "reference": "Awaiting at least two human approvals.",
                            }
                        ],
                    },
                }
            ]
        }
    if phase == "4":
        return {
            "narrative_system": {
                "meta_narrative": {
                    "statement": "Core narrative statement",
                    "supported_values": ["value_name"],
                },
                "storylines": {
                    "products": "Product storyline",
                    "services": "Service storyline",
                    "ai_agents": "Agent storyline",
                    "community": "Community storyline",
                },
                "dynamic_rules": [
                    {
                        "if": "condition",
                        "then": "modulation",
                        "while": "value constraint",
                    }
                ],
            }
        }
    if phase == "5":
        return {
            "co_creation": {
                "consensus_areas": ["agreed area"],
                "divergences": [
                    {
                        "topic": "open topic",
                        "positions": ["position A", "position B"],
                        "minority_voices": ["voice statement"],
                    }
                ],
                "accepted_changes": ["accepted change"],
                "rejected_changes": ["rejected change"],
                "dissent_log": ["dissent note"],
            }
        }
    if phase == "6":
        return {
            "guardian_report": {
                "quarter": "2026-Q1",
                "scenario_alignment": {
                    "confirming": ["confirming signal"],
                    "contradicting": ["contradicting signal"],
                    "emerging": ["emerging signal"],
                },
                "coherence": {
                    "consistent": ["consistent behavior"],
                    "inconsistent": ["inconsistent behavior"],
                },
                "divergence_level": "drift",
                "recommended_action": "correct",
            }
        }
    raise ValueError(f"unsupported phase `{phase}`")


class SpeculaOrchestrator:
    """State-aware orchestrator that emits validated artifacts."""

    def __init__(self, state: ProjectState, llm_client: LLMClient | None = None) -> None:
        self.state = state
        self.llm_client = llm_client

    def generate_step(self, user_input: str, phase: str | None = None, mode: str | None = None) -> Dict[str, Any]:
        if not user_input or not user_input.strip():
            raise ValueError("user_input cannot be empty")

        selected_phase = str(phase or self.state.current_phase)
        if selected_phase not in PHASE_SEQUENCE:
            raise ValueError(f"invalid phase `{selected_phase}`")
        self._assert_phase_prerequisites(selected_phase)

        selected_mode = mode or PHASE_DEFAULT_MODE[selected_phase]

        artifact_id = f"artifact-{uuid4()}"
        related_artifacts: List[str] = [
            self.state.latest_artifacts[key]
            for key in sorted(self.state.latest_artifacts.keys())
            if self.state.latest_artifacts.get(key)
        ]

        artifact = {
            "meta": {
                "artifact_id": artifact_id,
                "phase": selected_phase,
                "mode": selected_mode,
                "generated_at": _now_iso(),
                "validated_by_human": False,
                "related_artifacts": related_artifacts,
                "decision_rationale": f"Draft generated for phase {selected_phase} pending human review.",
                "evidence_refs": ["session_input:user"],
                "tradeoffs": ["Speed of synthesis vs depth of validation remains open."],
                "rejected_alternatives": ["No alternative path selected before human validation."],
            },
            "payload": build_payload_template(selected_phase, selected_mode),
        }

        assistant_text = self._build_assistant_text(
            phase=selected_phase,
            mode=selected_mode,
            user_input=user_input,
        )

        text_errors = validate_assistant_text(assistant_text)
        if text_errors:
            raise ValueError("assistant text validation failed:\n" + "\n".join(text_errors))

        assert_artifact_valid(artifact, current_phase=selected_phase)
        self.state.latest_artifacts[selected_phase] = artifact_id
        self.state.artifact_index[artifact_id] = artifact

        return {
            "assistant_text": assistant_text,
            "artifact": artifact,
        }

    def _build_assistant_text(self, *, phase: str, mode: str, user_input: str) -> str:
        fallback = "\n".join(
            [
                f"MODE: {mode} | PHASE: {phase}",
                _framing_for_phase(phase),
                _question_for_phase(phase),
            ]
        )

        if self.llm_client is None:
            return fallback

        try:
            candidate = self.llm_client.generate_assistant_text(
                phase=phase,
                mode=mode,
                user_input=user_input,
                project_id=self.state.project_id,
                context_bundle=self._build_context_bundle(),
            ).strip()
        except LLMProviderError:
            return fallback

        # Normalize output if provider omitted canonical header.
        if not candidate.startswith("MODE: "):
            candidate = f"MODE: {mode} | PHASE: {phase}\n{candidate}"

        if validate_assistant_text(candidate):
            return fallback
        return candidate

    def advance_after_validation(
        self,
        phase: str,
        artifact_id: str,
        validations: List[Dict[str, Any]],
    ) -> str:
        phase = str(phase)
        if phase != self.state.current_phase:
            raise ValueError(
                f"phase mismatch: current phase is `{self.state.current_phase}` but received `{phase}`"
            )
        artifact = self.state.artifact_index.get(artifact_id)
        if artifact is None:
            raise ValueError(f"artifact `{artifact_id}` is not available in state context")
        self._assert_validation_requirements(artifact_id=artifact_id, validations=validations)

        self.state.latest_artifacts[phase] = artifact_id
        self.state.phase_validated_artifacts[phase] = artifact_id
        self._update_continuity_context(phase=phase, artifact=artifact, validations=validations)
        next_phase = NEXT_PHASE[phase]
        self.state.current_phase = next_phase
        return next_phase

    def _assert_phase_prerequisites(self, phase: str) -> None:
        required = PHASE_PREREQUISITES[phase]
        missing = [item for item in required if item not in self.state.phase_validated_artifacts]
        if missing:
            raise ValueError(
                f"cannot generate phase `{phase}` without validated prerequisite phases: {', '.join(missing)}"
            )

    def _assert_validation_requirements(
        self, *, artifact_id: str, validations: List[Dict[str, Any]]
    ) -> None:
        approved_human = [
            row
            for row in validations
            if bool(row.get("validated_by_human"))
            and str(row.get("decision", "")).lower() == "approve"
        ]
        if len(approved_human) < 2:
            raise ValueError(
                f"artifact `{artifact_id}` requires at least two human approvals to advance"
            )

        unique_roles = {
            str(row.get("validator_role", "")).strip().lower()
            for row in approved_human
            if str(row.get("validator_role", "")).strip()
        }
        if len(unique_roles) < 2:
            raise ValueError(
                f"artifact `{artifact_id}` requires approvals from at least two distinct validator roles"
            )

    def _build_context_bundle(self) -> Dict[str, Any]:
        validated = sorted(
            self.state.phase_validated_artifacts.items(),
            key=lambda item: _phase_sort_key(item[0]),
        )
        recent = []
        for phase, artifact_id in validated[-4:]:
            artifact = self.state.artifact_index.get(artifact_id, {})
            recent.append(
                {
                    "phase": phase,
                    "artifact_id": artifact_id,
                    "mode": artifact.get("meta", {}).get("mode"),
                    "payload": artifact.get("payload", {}),
                }
            )
        return {
            "validated_phases": [phase for phase, _ in validated],
            "continuity_context": self.state.continuity_context,
            "recent_validated_artifacts": recent,
        }

    def _update_continuity_context(
        self,
        *,
        phase: str,
        artifact: Dict[str, Any],
        validations: List[Dict[str, Any]],
    ) -> None:
        payload = artifact.get("payload", {})
        mode = artifact.get("meta", {}).get("mode")
        approver_roles = sorted(
            {
                str(row.get("validator_role", "")).strip()
                for row in validations
                if bool(row.get("validated_by_human"))
                and str(row.get("decision", "")).lower() == "approve"
                and str(row.get("validator_role", "")).strip()
            }
        )
        self._append_continuity(
            "decision_log",
            f"Phase {phase} validated with approver roles: {', '.join(approver_roles)}.",
        )

        if phase == "2":
            brand_dna = payload.get("brand_dna", {})
            for item in brand_dna.get("radical_values", []):
                value = str(item.get("value", "")).strip()
                self._append_continuity("radical_values", value)

        if phase == "3" and mode == "refusal_register":
            for refusal in payload.get("refusals", []):
                signal = str(refusal.get("identity_signal", "")).strip()
                violated = str(refusal.get("violated_value", "")).strip()
                self._append_continuity("refusal_signals", signal)
                self._append_continuity("open_assumptions", violated)

        if phase == "3" and mode in {"prototyping", "ethical_gate"}:
            for prototype in payload.get("prototypes", []):
                gate = prototype.get("ethical_gate", {})
                status = str(gate.get("status", "")).strip()
                description = str(prototype.get("description", "")).strip()
                if status and status != "PASS":
                    self._append_continuity(
                        "open_assumptions",
                        f"Prototype `{description or prototype.get('prototype_id', '')}` remains `{status}`.",
                    )

        if phase == "6":
            coherence = payload.get("guardian_report", {}).get("coherence", {})
            for inconsistent in coherence.get("inconsistent", []):
                self._append_continuity("open_assumptions", str(inconsistent).strip())

    def _append_continuity(self, key: str, value: str, max_items: int = 25) -> None:
        if not value:
            return
        bucket = self.state.continuity_context.setdefault(key, [])
        if value not in bucket:
            bucket.append(value)
        if len(bucket) > max_items:
            del bucket[:-max_items]
