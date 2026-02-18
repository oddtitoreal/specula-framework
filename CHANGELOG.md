# Changelog

All notable changes to this repository are documented here.

## Unreleased
### 2026-02-18 - executable agent MVP enablement
- Added an executable Python runtime in `src/specula_agent/` with:
  - state-aware orchestrator and phase transition gate (`orchestrator.py`)
  - policy checks for one-question rule, output header, anti-oracular language, and 6-line pre-question limit (`policy.py`)
  - JSON Schema-driven artifact validation (`schemas.py`)
  - CLI commands for `step`, `validate`, and `advance` (`cli.py`)
- Added machine-readable canonical contracts under `schemas/`:
  - `phase0_activation.schema.json`
  - `phase1_scenarios.schema.json`
  - `phase1_5_competitive_map.schema.json`
  - `phase2_brand_dna.schema.json`
  - `phase3_prototypes.schema.json`
  - `phase3_refusals.schema.json`
  - `phase4_narrative_system.schema.json`
  - `phase5_cocreation.schema.json`
  - `phase6_guardian.schema.json`
- Added executable test suite in `tests/` for schema/meta validation, non-oracular checks, and state transition behavior.
- Added provider adapters for real LLM generation (`openai`, `anthropic`) in `src/specula_agent/llm.py`, with strict fallback to deterministic output if policy constraints are violated.
- Added optional PostgreSQL persistence and audit logging in `src/specula_agent/storage.py`, plus exportable SQL in `sql/specula_persistence.sql`.
- Extended CLI with `init-db`, `--database-url`, and LLM flags (`--llm-provider`, `--llm-model`, `--llm-api-key-env`, `--llm-base-url`).
- Added CI workflow in `.github/workflows/ci.yml` to run automated tests on push and pull requests.
- Added packaging metadata (`pyproject.toml`) with optional `postgres` dependency and a runtime hygiene ignore file (`.gitignore`).
- Added a reusable base prompt in `prompts/specula_method_agent_base.md`, derived from `specula-method/agent/specula-method-agent.md` and aligned to canonical `specula-framework` constraints.
- Updated `README.md` with runtime assets map and local MVP quickstart (`venv`, install, CLI run, pytest).
- Updated `docs/00_index.md` with links to runtime assets (`schemas/`, `prompts/`).
- Aligned `docs/05_system_architecture_inputs.md` to canonical schema contract naming from `docs/06_json_schemas_outputs.md` (phase keys, refusal artifact naming, and phase references).
- Updated `docs/13_specula_method_agent.md` to reflect canonical phase sequence (0, 1, 1.5, 2, 3, 4, 5, 6) and canonical artifact wrapper terminology.

### 2026-02-18 - v2.4.5.2 alignment assessment and integration
- Added `docs/14_specula_method_v2_4_5_2_aligned.md` as a non-normative aligned proposal for a possible next framework version.
- Marked the proposal explicitly as `Version: 2.4.5.2`, dated `2026-02-18`, with status `Proposal (non-normative; compatibility layer with framework v2.3)`.
- Updated `docs/00_index.md` and `README.md` to include the v2.4.5.2 proposal in the documentation navigation.
- Added missing version/date headers to `specs/terminology.md` and `docs/13_specula_method_agent.md` for policy compliance.
- Aligned the Agent Protocol output contract with MVP validation tests by changing the summary constraint from 10 lines to 6 lines before the next question.
- Removed the stale changelog entry that referenced a `case-saponaria` placeholder directory that is not present in the repository.
- Structural impact assessment: no change to canonical normative documents (`docs/01`-`docs/08`, `specs/precedence.md`, `specs/versioning.md`), no change to canonical schema contracts in `docs/06_json_schemas_outputs.md`, and no change to the current control logic/state machine.
- Operational impact assessment: low immediate impact (documentation/navigation/governance hygiene), medium migration impact only if v2.4.5.2 is later promoted from proposal to canonical framework version.
- Initial private delivery scaffold.
- Added version/date headers to core documents.
- Added version/date headers to governance specs.
- Standardized mode identifiers and schema enums.
- Aligned dataset annotation cognitive_mode values with canonical modes.
- Aligned schema traceability fields and phase input enum.
- Updated template meta wrapper mode enum to canonical list.
- Added MVP implementation guide for AI engineers.
- Added MVP sample conversations with expected JSON artifacts.
- Added MVP validation test checklist for non-oracularity and format.
- Added MVP persistence schema for Refusal Register and Guardian.
- Updated documentation index to include implementation docs.
- Added Specula Method Agent Protocol overview document.
- Updated README and docs index to include the agent protocol.

## 2026-01-24
- Repository structure created.
- Imported English documentation set into `docs/`.
