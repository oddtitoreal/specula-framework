# Changelog

All notable changes to the SPECULA Framework canonical source are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-03-27

### Added

**Runtime Learning Loops & Guardian Agency**
- Refusal Register Learning Loop: `refusal_learning` key to `continuity_context` with structured entries (`refusal_id`, `violated_value`, `identity_signal`, `date`, `review_after`). Enables re-evaluation of past refusals at +90 day intervals rather than pure archival.
- `SpeculaOrchestrator.refusals_due_for_review(reference_date)` public method for periodic re-evaluation workflow.
- Guardian Loop Agency: `GUARDIAN_CRITICAL_LEVELS` and `GUARDIAN_RESPÉCULATE_ACTIONS` module constants. Critical drift now generates mandatory `GUARDIAN ALERT` entries to both `decision_log` and `open_assumptions`.
- Phase 5 structural enforcement: `co_creation.dissent_log` and `co_creation.rejected_changes` now mandatory, preventing theater consultation patterns.

**Documentation & Governance**
- `docs/15_circolo_di_sintesi_governance.md` — Circolo di Sintesi Governance Charter: 5-role composition, unanimous/4-5/3-5/veto voting rules, 24-month terms, quorum fallback procedures, organizational capture safeguards.
- `docs/16_refusal_register_learning_loop.md` — Learning Loop Protocol: technical integration with orchestrator, 3-question re-evaluation process, decision log format, review frequency guidance.

### Changed
- Imports: added `timedelta` and `Optional` for learning loop time handling.
- Phase 6 continuity context now includes Guardian alert write-through for `critical` divergence levels.

## [1.1.1] - 2026-02-19

### Added

**Governance & Explainability**
- Validation record governance fields: `validator_role`, `decision`, unique constraint on `(artifact_id, validator_id)` for duplicate-signature prevention.
- Continuity memory context and validated-phase prerequisites in runtime orchestration.
- Mandatory explainability metadata across all phase schemas: `decision_rationale`, `evidence_refs`, `tradeoffs`, `rejected_alternatives`.

### Changed
- Phase advancement now requires at least two human approvals from distinct validator roles (`src/specula_agent/orchestrator.py`, `src/specula_agent/cli.py`).
- Phase 3 contract strengthened: explicit rationale required for each Ethical Gate question with reviewer decision references.
- Persistence and SQL export aligned to governance schema changes (`src/specula_agent/storage.py`, `sql/specula_persistence.sql`).
- Updated normative documentation to reflect governance runtime contract (`docs/06_json_schemas_outputs.md`, `docs/13_specula_method_agent.md`).

## [1.1.0] - 2026-02-18

### Added

**Executable Runtime MVP**
- Python runtime framework in `src/specula_agent/`:
  - State-aware orchestrator and phase transition gate (`orchestrator.py`)
  - Policy validator: one-question rule, output header, anti-oracular language, 6-line pre-question limit (`policy.py`)
  - JSON Schema-driven artifact validation (`schemas.py`)
  - CLI commands: `step`, `validate`, `advance` (`cli.py`)

**Machine-Readable Canonical Contracts**
- Phase schemas in `schemas/`:
  - `phase0_activation.schema.json`
  - `phase1_scenarios.schema.json`
  - `phase1_5_competitive_map.schema.json`
  - `phase2_brand_dna.schema.json`
  - `phase3_prototypes.schema.json`
  - `phase3_refusals.schema.json`
  - `phase4_narrative_system.schema.json`
  - `phase5_cocreation.schema.json`
  - `phase6_guardian.schema.json`

**Executable Validation & Testing**
- Test suite in `tests/` for schema validation, meta validation, non-oracular checks, state transition behavior.
- LLM provider adapters (`openai`, `anthropic`) in `src/specula_agent/llm.py` with deterministic fallback.
- Optional PostgreSQL persistence and audit logging (`src/specula_agent/storage.py`).
- SQL export schema in `sql/specula_persistence.sql`.

**DevOps & Packaging**
- CLI extensions: `init-db`, `--database-url`, `--llm-provider`, `--llm-model`, `--llm-api-key-env`, `--llm-base-url`.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) for schema validation and link tests.
- Packaging metadata in `pyproject.toml` with optional `postgres` dependency.

**Documentation & Alignment**
- Base prompt in `prompts/specula_method_agent_base.md` (derived from `specula-method` and aligned to `specula-framework` constraints).
- `docs/14_specula_method_v2_4_5_2_aligned.md` — non-normative v2.4.5.2 proposal as compatibility layer.
- Runtime alignment guide: `docs/05_system_architecture_inputs.md` and `docs/06_json_schemas_outputs.md` updated for canonical phase sequence and artifact wrapper terminology.
- `docs/13_specula_method_agent.md` updated to canonical phase sequence (0, 1, 1.5, 2, 3, 4, 5, 6) and deployment notes.
- Documentation index updated with runtime assets and agent protocol.

### Changed
- Agent Protocol output contract: summary constraint updated from 10 lines to 6 lines.
- Core documents now include version/date headers (`specs/terminology.md`, `docs/13_specula_method_agent.md`).
- Mode identifiers and schema enums standardized across runtime and templates.

## [1.0.0] - 2026-01-24

### Added
- Repository structure and canonical documentation set in `docs/`.
- Specs foundation: `specs/precedence.md`, `specs/terminology.md`, `specs/versioning.md`.
- Documentation layers:
  - Conceptual foundations (`docs/01`-`docs/08`)
  - Technical translation (`docs/09`-`docs/13`)
  - Governance charter placeholders for future expansion

---

## Version History Notes

**Version 1.0.0** establishes the canonical SPECULA Framework as the single source of truth for runtime contracts, schemas, and governance specifications.

**Version 1.1.0** introduced the executable Python MVP, making the framework operationalizable via CLI and API. Schemas became machine-readable contracts rather than documentation artifacts.

**Version 1.1.1** hardened governance by enforcing dual-signature validation and explainability metadata across all artifacts — moving the framework from "documented design" to "auditable runtime."

**Version 1.2.0** completed the learning loop architecture (Refusal Register re-evaluation, Guardian alerting) and added the Circolo di Sintesi governance model, making the framework self-governing and responsive to operational drift.

**Major versions** (2.0.0+) will be released for:
- Fundamental restructuring of the phase architecture
- Breaking changes to schema contracts or specification precedence
- New governance layers or framework-wide protocol changes

**Minor versions** (1.x.0) for:
- New runtime capabilities (executors, integrations, learning loops)
- New documentation layers or case studies
- Significant schema additions (new phase templates, new fields)

**Patch versions** (1.x.y) for:
- Schema compatibility fixes
- Documentation clarifications
- Non-breaking runtime improvements
