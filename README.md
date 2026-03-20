# SPECULA Framework

This repository is the **canonical SPECULA source** for docs, specs, schemas, and runtime profile.
It originated from a client delivery and is now maintained as the ecosystem reference repository.

## SPECULA Ecosystem

This repository is one of three related SPECULA repositories:

| Repository | Primary purpose | Primary audience |
|---|---|---|
| `specula-framework` (this repo) | Canonical docs/specs/schemas/runtime profile | Governance architects, contributors, technical leads |
| [`specula-method`](https://github.com/oddtitoreal/specula-method) | Strategic foresight branding method | Strategists, designers, innovation teams |
| [`specula-skill`](https://github.com/oddtitoreal/specula-skill) | Constitution/state-machine implementation skill | AI engineers, governance implementers |

Entry points:
- If you need canonical governance specs and runtime contracts: start here.
- If you need facilitation and method process: go to `specula-method`.
- If you need technical constitution/state-machine implementation examples: go to `specula-skill`.

## Who This Is For

- Governance researchers and framework contributors
- Technical architects integrating SPECULA runtime contracts
- Teams needing canonical terminology/spec/version references

## Recommended reading order
1. Foundations of the Specula Method
2. SPECULA AI Constitution
3. Technical Translation & Operational Governance
4. Control Logic & State Machine
5. System Architecture & Input Specifications
6. JSON Schemas & Output Architecture
7. Prompt Playbook v1.0
8. Specula Method v2.3
9. Specula Method Agent Protocol
10. Specula Method v2.4.5.2 (Aligned Proposal, IT)

## Repository map
- `docs/` — canonical documents (human-readable)
- `specs/` — governance specs (precedence, terminology, versioning, compliance)
- `schemas/` — machine-readable JSON schemas (runtime contracts)
- `prompts/` — system + phase prompt templates
- `src/` — executable runtime MVP (`specula_agent`)
- `tests/` — executable validation and orchestrator tests
- `templates/` — example payloads and project scaffolding

## Governance
See `specs/precedence.md` and `specs/terminology.md`.
See `ALIGNMENT.md` for cross-repository ownership and sync rules.

## Versioning
See `specs/versioning.md` and `CHANGELOG.md`.
See `VERSIONS.md` for the multi-repository version map.

## Runtime MVP (Local)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
specula-agent step --user-input "Start Phase 0 for a new project"
pytest
```

## Runtime with LLM + PostgreSQL (Optional)
```bash
source .venv/bin/activate
python -m pip install -e .[postgres]
export OPENAI_API_KEY="..."
export SPECULA_DATABASE_URL="postgresql://user:pass@localhost:5432/specula"
specula-agent init-db --database-url "$SPECULA_DATABASE_URL"
specula-agent step \
  --user-input "Start Phase 1 for a mobility brand" \
  --llm-provider openai \
  --llm-model gpt-4o-mini \
  --llm-api-key-env OPENAI_API_KEY \
  --database-url "$SPECULA_DATABASE_URL"
```

> Delivery date: 2026-01-04
