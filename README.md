# SPECULA Framework

*The canonical source of truth for AI governance contracts, runtime specifications, and schema definitions.*

This repository is the **runtime reference layer** of the SPECULA ecosystem. It maintains the authoritative definitions for governance schemas, phase contracts, persistence models, and executable validation rules that keep all SPECULA implementations coherent and interoperable.

> **New here?** Start from the [Quick Start guide](./QUICKSTART.md) · [Avvio rapido (IT)](./QUICKSTART.it.md)

## What This Repository Is

**specula-framework** is the single source of truth for:
- **JSON Schema contracts** for all 6 phases and runtime artifacts
- **Canonical phase specifications** (sequence, validation gates, advancement rules)
- **Governance precedence** and terminology standards
- **Executable runtime** (`specula_agent`) for phase orchestration and validation
- **Persistence models** for audit logging and continuity context
- **Explainability requirements** and metadata standards

It defines *how* governance works at runtime. Other repos define the method and specific implementations; this repo defines the contracts that keep them aligned.

## SPECULA Ecosystem

This repository is one of three related SPECULA repositories:

| Repository | Primary Role | Entry Point |
|---|---|---|
| `specula-framework` (this repo) | **Runtime specification layer** — canonical schemas, contracts, executable validation | If you're integrating SPECULA into a system, building a runtime, or need authoritative specs |
| [`specula-method`](https://github.com/oddtitoreal/specula-method) | **Methodology layer** — the six-phase facilitation process, ethical framework, decision logic | If you need to understand the method itself or run a facilitated session |
| [`specula-skill`](https://github.com/oddtitoreal/specula-skill) | **Implementation layer** — constitution validation, state-machine templates, constitution-to-runtime mapping | If you're implementing SPECULA governance rules in code |

## Start Here If You Need To...

- **Integrate SPECULA** into a production system → Read `docs/05_system_architecture_inputs.md` and `docs/06_json_schemas_outputs.md`
- **Understand the canonical phase sequence** → See `specs/terminology.md` and the JSON schemas in `schemas/`
- **Run a SPECULA governance session** → Use `specula-method` (this repo provides the runtime)
- **Implement governance rules** → Use `specula-skill` with the canonical contracts from here
- **Contribute to the framework** → See `CONTRIBUTING.md` and `specs/precedence.md`
- **Understand governance precedence** → Read `specs/precedence.md` and `ALIGNMENT.md`

## Recommended Reading Order

1. **What is SPECULA?** → `specula-method` overview
2. **What phases are there?** → `docs/00_index.md`, then read `docs/01`-`docs/08` (conceptual foundations)
3. **What do artifacts look like?** → `docs/06_json_schemas_outputs.md` and the schemas in `schemas/`
4. **How does the runtime work?** → `docs/13_specula_method_agent.md` and `docs/14_specula_method_v2_4_5_2_aligned.md`
5. **What are the governance rules?** → `docs/09`-`docs/12` (technical translation & control logic)
6. **How do we maintain alignment?** → `specs/`, `ALIGNMENT.md`, `VERSIONS.md`

## Repository Structure

- **`docs/`** — canonical specifications (conceptual → technical → governance)
  - `01`-`08` — conceptual foundations (phases, ethical gates, identity, impact)
  - `09`-`13` — technical translation (system architecture, schemas, agent protocol)
  - `14`-`16` — governance & learning (v2.4.5.2 proposal, governance charter, refusal loops)
- **`schemas/`** — machine-readable runtime contracts (JSON Schema for each phase + artifacts)
- **`specs/`** — precedence, terminology, and versioning rules for the entire framework
- **`src/specula_agent/`** — executable Python runtime for phase orchestration and validation
- **`prompts/`** — canonical prompt templates aligned to phase contracts
- **`templates/`** — example payloads and project scaffolding for new implementations
- **`tests/`** — executable validation suite (schema tests, policy checks, state transitions)
- **`sql/`** — persistence schemas for audit logging and continuity context

## Governance & Alignment

See:
- **`specs/precedence.md`** — which specs override others in case of conflict
- **`specs/terminology.md`** — canonical term definitions (phase, phase-id, schema, etc.)
- **`specs/versioning.md`** — framework versioning policy
- **`ALIGNMENT.md`** — cross-repository ownership rules (who maintains what)
- **`VERSIONS.md`** — version matrix across all three repos

## Version & Changelog

See:
- **`CHANGELOG.md`** — release history with semver tags and formal change documentation
- **`VERSIONS.md`** — version alignment across specula-method, specula-skill, specula-framework

Current version: **1.2.0** (2026-03-27)

## Getting Started Locally

### Minimal Local Runtime

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
specula-agent step --user-input "Start Phase 0 for a new project"
pytest
```

### Full Runtime (with LLM + PostgreSQL)

```bash
source .venv/bin/activate
python -m pip install -e .[postgres]
export OPENAI_API_KEY="your-api-key"
export SPECULA_DATABASE_URL="postgresql://user:pass@localhost:5432/specula"
specula-agent init-db --database-url "$SPECULA_DATABASE_URL"
specula-agent step \
  --user-input "Start Phase 1 for a new organization" \
  --llm-provider openai \
  --llm-model gpt-4o \
  --llm-api-key-env OPENAI_API_KEY \
  --database-url "$SPECULA_DATABASE_URL"
```

## How to Contribute

See `CONTRIBUTING.md` and `specs/precedence.md`. Key principles:
- Schema changes require dual review (framework lead + spec maintainer)
- Phase contract changes are breaking and require minor version bump
- Documentation clarifications can be patch versions
- All contributions must pass the test suite in `tests/`

## License & Attribution

See `LICENSE.md` and `ATTRIBUTION.md`. The SPECULA Framework is distributed under CC BY-SA 4.0.

---

**Last updated:** 2026-03-29  
**Repository role:** Canonical runtime specification layer of SPECULA ecosystem
