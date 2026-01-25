# SPECULA AI – IMPLEMENTATION GUIDE (MVP)

Version: 1.0
Date: 2026-01-24

This document translates the SPECULA framework into a minimal, buildable
implementation blueprint for AI engineers. It does not replace normative
documents; it makes them executable.

---

## 1. System Objectives (Operational)

The system must:
- Enforce phase gating and human validation.
- Preserve non-oracular behavior (questions over answers).
- Produce artifacts that conform to the JSON schemas.
- Persist Refusal Register and Guardian outputs as long-lived constraints.

Non-goals for MVP:
- Fine-tuning or model training.
- Automated ethical decisions.
- Full UI/UX specification.

---

## 2. Architecture Overview

### Components
1) **Orchestrator**: controls phase, mode, routing, and gate checks.
2) **LLM Adapter**: handles prompts and post-processing.
3) **Validation Layer**: schema validation + non-oracular checks.
4) **Storage**: artifact store + Refusal Register + Guardian reports.
5) **Human Gate Service**: UI or API to validate artifacts.

### Data Flow (happy path)
1) User input -> Orchestrator sets phase + mode.
2) LLM Adapter generates output.
3) Validation Layer checks schema + policies.
4) If valid -> Persist artifact -> Ask for human validation.
5) If validated -> Phase transition allowed; else -> halt.

---

## 3. State Model

### State Object (in memory)
```json
{
  "project_id": "uuid",
  "current_phase": "0|1|1.5|2|3|4|5|6",
  "current_mode": "exploration|convergence|brand_archaeology|prototyping|ethical_gate|refusal_register|narrative_synthesis|community_cocreation|guardian|cognitive_sparring|sensemaking|slowdown|refusal",
  "latest_artifacts": {
    "phase_1": "artifact_id",
    "phase_1_5": "artifact_id",
    "phase_2": "artifact_id",
    "phase_3": "artifact_id",
    "phase_4": "artifact_id",
    "phase_5": "artifact_id",
    "phase_6": "artifact_id"
  }
}
```

### Phase Transitions
Use the state machine defined in `docs/04_control_logic.md`.
Hard-stop when `validated_by_human == false`.

---

## 4. Prompt Assembly (MVP)

### Inputs to the LLM
- System prompt core from `docs/03_technical_governance.md`.
- Phase-specific constraints (from `docs/07_prompt_playbook_v1.md`).
- Current phase + mode.
- Refusal Register excerpts (if any).

### Output Format Contract
Every response must:
- Declare `MODE | PHASE` at the top.
- Ask exactly one question.
- Conform to the schema wrapper in `docs/06_json_schemas_outputs.md`.

---

## 5. Validation Layer

### Required Checks (blocking)
1) JSON schema validation for the current phase.
2) `meta.phase` matches orchestrator `current_phase`.
3) `meta.mode` in canonical enum (see `specs/terminology.md`).
4) `validated_by_human == false` for newly generated artifacts.
5) One-question rule:
   - Exactly one `?` in the final user-facing text.
   - No directives like "choose", "decide", "best option".

### Non-oracularity Heuristics (blocking)
Reject or rewrite if:
- Contains definitive prescriptions ("you should", "the correct choice").
- Contains rankings as final decisions.
- Contains `decision: true`.

---

## 6. Human Validation Gate

### Required Fields
- `artifact_id`
- `phase`
- `decision`: `validated_by_human = true|false`
- `validator_id`
- `validated_at`

No phase transition is allowed unless validation is true for all prerequisite
artifacts (see `docs/04_control_logic.md`).

---

## 7. Persistence Model

### Minimum Collections / Tables
- `projects` (state, metadata)
- `artifacts` (all phase outputs)
- `refusal_register` (immutable)
- `guardian_reports` (quarterly)
- `validations` (human decisions)

### Artifact Storage
Store the full JSON wrapper: `{ meta, payload }`.

---

## 8. Error Handling

### On Schema Failure
- Return a system error to the orchestrator.
- Retry with schema-guided correction prompt.

### On Non-oracular Violation
- Trigger `slowdown` or `refusal` mode.
- Require human acknowledgment.

---

## 9. Observability & Audit

Log:
- All prompts and responses (with PII policy).
- All validation results and gate decisions.
- All phase transitions.

Keep immutable history for compliance and for Guardian checks.

---

## 10. Security & Privacy (Minimum)

- No external data sources without explicit approval.
- Store only necessary metadata.
- Redact sensitive inputs in logs when possible.

---

## 11. MVP Readiness Checklist

- [ ] Orchestrator enforces phase gates.
- [ ] JSON schema validation passes for every artifact.
- [ ] Non-oracularity checks in place.
- [ ] Human validation UI/API available.
- [ ] Refusal Register and Guardian persistence implemented.
