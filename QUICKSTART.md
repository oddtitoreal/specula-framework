# Quick Start

**Your AI governance is distributed across prompts, documents, and informal decisions. Teams interpret it differently. When edge cases arise, there's no source of truth.**

This is the canonical layer: runtime contracts, schemas, and specs that keep distributed SPECULA implementations coherent.

## What this repo gives you

- **Schemas**: machine-readable JSON contracts for constitutions and state machines
- **Specs**: terminology, versioning, precedence rules, compliance guidelines
- **Runtime MVP**: local execution of a SPECULA agent
- **Sample conversations**: how the runtime behaves across phases

## Start here based on what you need

| I need to... | Go to |
|---|---|
| Validate existing governance artifacts | [`specula-skill`](https://github.com/oddtitoreal/specula-skill) |
| Run the method with a client | [`specula-method`](https://github.com/oddtitoreal/specula-method) |
| Integrate SPECULA into a production system | [docs/09_implementation_guide.md](./docs/09_implementation_guide.md) |
| Understand canonical schemas and specs | You're in the right place |

## Run the runtime MVP (5 min)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
specula-agent step --user-input "Start Phase 0 for a new project"
pytest
```

## In practice

The canonical schemas in this repo underpin the governance artifacts for *Il posto delle fragole* — a real community space brand built in Pesaro using the Specula Method. The process went from participatory co-design to brand identity to validated constitution and state machine.

→ [Case study in specula-method](https://github.com/oddtitoreal/specula-method/tree/main/case-studies/case_study_posto_delle_fragole.md)
→ [Governance artifacts in specula-skill](https://github.com/oddtitoreal/specula-skill/tree/main/examples/community-space-brand)

## What next?

- **Full documentation map**: [docs/00_index.md](./docs/00_index.md)
- **Governance specs**: [specs/](./specs/)
- **Runtime implementation guide**: [docs/09_implementation_guide.md](./docs/09_implementation_guide.md)
