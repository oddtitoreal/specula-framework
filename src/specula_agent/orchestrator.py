"""Minimal executable orchestrator for Specula agent sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from .constants import NEXT_PHASE, PHASE_DEFAULT_MODE, PHASE_SEQUENCE
from .llm import LLMClient, LLMProviderError
from .policy import validate_assistant_text
from .schemas import assert_artifact_valid


@dataclass
class ProjectState:
    """In-memory state used by the orchestrator."""

    project_id: str
    current_phase: str = "0"
    latest_artifacts: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectState":
        return cls(
            project_id=data["project_id"],
            current_phase=str(data.get("current_phase", "0")),
            latest_artifacts=dict(data.get("latest_artifacts", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "current_phase": self.current_phase,
            "latest_artifacts": self.latest_artifacts,
        }


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


def build_payload_template(phase: str) -> Dict[str, Any]:
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
            },
            "payload": build_payload_template(selected_phase),
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
            ).strip()
        except LLMProviderError:
            return fallback

        # Normalize output if provider omitted canonical header.
        if not candidate.startswith("MODE: "):
            candidate = f"MODE: {mode} | PHASE: {phase}\n{candidate}"

        if validate_assistant_text(candidate):
            return fallback
        return candidate

    def advance_after_validation(self, phase: str, artifact_id: str, validated_by_human: bool) -> str:
        phase = str(phase)
        if phase != self.state.current_phase:
            raise ValueError(
                f"phase mismatch: current phase is `{self.state.current_phase}` but received `{phase}`"
            )
        if not validated_by_human:
            raise ValueError("cannot advance while validated_by_human is false")

        self.state.latest_artifacts[phase] = artifact_id
        next_phase = NEXT_PHASE[phase]
        self.state.current_phase = next_phase
        return next_phase
