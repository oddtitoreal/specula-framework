# Avvio rapido

**La governance del tuo sistema AI è distribuita tra prompt, documenti e decisioni informali. I team la interpretano diversamente. Quando emergono casi limite, non c'è una fonte unica di verità.**

Questo è il livello canonico: contratti runtime, schemi e specifiche che mantengono coerenti le implementazioni SPECULA distribuite.

## Cosa offre questo repository

- **Schemi**: contratti JSON machine-readable per constitution e state machine
- **Specifiche**: terminologia, versionamento, regole di precedenza, linee guida di compliance
- **Runtime MVP**: esecuzione locale di un agente SPECULA
- **Conversazioni di esempio**: come il runtime si comporta nelle diverse fasi

## Parti da qui in base a cosa ti serve

| Ho bisogno di... | Vai a |
|---|---|
| Validare artefatti di governance esistenti | [`specula-skill`](https://github.com/oddtitoreal/specula-skill) |
| Applicare il metodo con un cliente | [`specula-method`](https://github.com/oddtitoreal/specula-method) |
| Integrare SPECULA in un sistema in produzione | [docs/09_implementation_guide.md](./docs/09_implementation_guide.md) |
| Comprendere schemi canonici e specifiche | Sei nel posto giusto |

## Eseguire il runtime MVP (5 min)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
specula-agent step --user-input "Start Phase 0 for a new project"
pytest
```

## In pratica

Gli schemi canonici di questo repository sono alla base degli artefatti di governance per *Il posto delle fragole* — un brand reale di spazio di comunità costruito a Pesaro con il Metodo Specula. Il processo è andato dal co-design partecipativo all'identità di brand fino a constitution e state machine validate.

→ [Case study in specula-method](https://github.com/oddtitoreal/specula-method/tree/main/case-studies/case_study_posto_delle_fragole.it.md)
→ [Artefatti di governance in specula-skill](https://github.com/oddtitoreal/specula-skill/tree/main/examples/community-space-brand)

## Prossimi passi

- **Mappa documentazione completa**: [docs/00_index.md](./docs/00_index.md)
- **Specifiche di governance**: [specs/](./specs/)
- **Guida all'implementazione**: [docs/09_implementation_guide.md](./docs/09_implementation_guide.md)
