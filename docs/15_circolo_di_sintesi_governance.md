# Circolo di Sintesi — Governance Charter
**Version**: 1.0
**Date**: 2026-03-27
**Status**: Normative (operational governance, not a canonical phase spec)
**Maintainer**: Specula Project Lead

---

## 1. Scopo

Il Circolo di Sintesi è l'organo decisionale sovrano dell'ecosistema Specula. Approva le decisioni di brand che implicano la AI Constitution, esercita il veto etico, e governa il Guardian Loop.

Questo documento colma il gap identificato nell'analisi integrata: il Circolo era definito come *what* (organo decisionale) ma non come *how* (composizione, voting, audit, fallback). Senza questo, il sistema crolla se il Circolo viene catturato o fallisce.

---

## 2. Composizione

Il Circolo è composto da **cinque ruoli distinti**, nessuno dei quali può essere ricoperto dalla stessa persona:

| Ruolo | Responsabilità | Requisiti |
|---|---|---|
| **Governance Architect** | Presidio della AI Constitution e dei principi normativi | Conoscenza approfondita del framework Specula |
| **Brand Strategist** | Presidio dell'identità di brand e della coerenza narrativa | Esperienza in branding strategico |
| **Ethics Reviewer** | Presidio degli impatti etici e delle conseguenze sistemiche | Background in etica applicata o design responsabile |
| **Community Advocate** | Presidio degli interessi delle comunità coinvolte | Relazione diretta con le comunità di riferimento del brand |
| **External Auditor** | Presidio dell'indipendenza del Circolo stesso | Esterno al progetto, ruolo rotante, nessun conflitto di interesse |

**Nota**: L'External Auditor è l'unico ruolo che non ha potere di voto ordinario, ma ha potere di **veto sospensivo** (vedi sezione 4).

---

## 3. Mandate e perimetro d'azione

Il Circolo delibera obbligatoriamente su:

- Avanzamento di fase dopo Phase 3 (Ethical Gate) con esito HOLD o REJECT
- Qualsiasi modifica ai `radical_values` dichiarati in Phase 2
- Decisioni di refusal che abbiano `opportunity_cost` classificato come "significativo"
- Guardian reports con `divergence_level: critical` o `recommended_action: re_speculate`
- Modifica o deroga a qualsiasi principio della AI Constitution
- Lancio di nuovi settori o mercati non previsti nel Speculative Identity Model

Il Circolo **non delibera** su:

- Decisioni operative quotidiane di brand (scelte di comunicazione, tone of voice specifiche)
- Step tecnici interni al workflow (i.e., quale schema JSON usare)
- Decisioni già validate attraverso il processo standard di dual-validation

---

## 4. Regole di voto

### 4.1 Unanimità (richiesta per)
- Modifica ai `radical_values` dichiarati
- Deroga a qualsiasi principio della AI Constitution
- Ammissione o rimozione di un membro del Circolo

### 4.2 Maggioranza qualificata (4/5, richiesta per)
- Avanzamento di fase con Ethical Gate in HOLD
- Guardian alert con `divergence_level: critical`
- Lancio in nuovi settori non previsti

### 4.3 Maggioranza semplice (3/5, richiesta per)
- Approvazione ordinaria di artifact di fase
- Modifica a policy operative (non costituzionali)

### 4.4 Veto sospensivo (External Auditor)
L'External Auditor può sospendere qualsiasi delibera per **72 ore** se rileva rischio di cattura organizzativa o conflitto di interesse non dichiarato. La sospensione richiede motivazione scritta. Dopo 72 ore la delibera può procedere senza il voto dell'Auditor se i quattro ruoli ordinari sono unanimi.

---

## 5. Rotation policy

Per prevenire calcificazione e cattura:

- **Term limit**: ogni ruolo ha durata massima di **24 mesi consecutivi**
- **Cooling-off**: dopo un term, non è possibile ricoprire lo stesso ruolo per almeno 12 mesi
- **External Auditor**: term di **12 mesi**, non rinnovabile consecutivamente
- **Onboarding**: ogni nuovo membro riceve un briefing di almeno 4 ore sul progetto Specula prima del primo voto

---

## 6. Meccanismo di audit

Il Circolo è auditabile dall'esterno attraverso:

1. **Decision Log pubblico**: ogni delibera produce una voce nel Decision Log con: data, materia, esito del voto (senza dettaglio dei voti individuali), rationale sintetico.
2. **Audit semestrale**: ogni 6 mesi, l'External Auditor produce un report indipendente sull'operato del Circolo, pubblicato insieme al Brand Radar Review.
3. **Trigger di audit straordinario**: se due o più decisioni del Circolo vengono contestate dalla community (via Community Co-Creation Protocol, sezione Escalation), si attiva un audit straordinario con auditor esterno aggiuntivo.

---

## 7. Fallback se il Circolo fallisce

**Scenario A — Impossibilità di quorum** (meno di 4 ruoli disponibili):
Le decisioni ordinarie sono sospese. Le decisioni urgenti (es. Guardian alert critico) possono essere prese temporaneamente dal Governance Architect + Ethics Reviewer con notifica pubblica e revisione obbligatoria alla ricomposizione del Circolo.

**Scenario B — Cattura organizzativa rilevata dall'Auditor**:
L'Auditor attiva procedura di freeze: nessuna delibera è valida fino alla nomina di un Circolo straordinario composto interamente da ruoli esterni al progetto. Durata massima del freeze: 30 giorni.

**Scenario C — Conflitto irrisolvibile (nessuna maggioranza raggiungibile)**:
La decisione viene sospesa e rimessa alla community (Phase 5 protocol) come input consultivo non vincolante. Il Circolo ha ulteriori 14 giorni per deliberare.

---

## 8. Relazione con il Guardian Loop

Il Guardian Loop (Phase 6) genera report con `divergence_level` e `recommended_action`. La relazione con il Circolo è la seguente:

| `divergence_level` | `recommended_action` | Azione del Circolo |
|---|---|---|
| `aligned` | `continue` | Nessuna azione richiesta |
| `drift` | `correct` | Informato, nessuna delibera obbligatoria |
| `significant_drift` | `escalate` | Delibera richiesta entro 30 giorni |
| `critical` | `re_speculate` | **Delibera urgente entro 7 giorni, ciclo di re-speculation obbligatorio** |

Quando il Guardian emette `divergence_level: critical`, il Circolo ha l'obbligo — non la facoltà — di deliberare. L'orchestratore registra questo obbligo nel `continuity_context.decision_log` (vedi `orchestrator.py`, `GUARDIAN_CRITICAL_LEVELS`).

---

## 9. Integrazione con il codice

L'orchestratore Specula implementa il requisito di dual-validation in `_assert_validation_requirements()`. Il Circolo di Sintesi è il **contesto umano e organizzativo** che dà significato a quel requisito tecnico: le due persone con ruoli distinti che approvano un artifact sono, idealmente, ruoli del Circolo o loro delegati formalmente nominati.

Il campo `validator_role` in ogni validation record deve corrispondere a uno dei cinque ruoli del Circolo (o a un ruolo delegato esplicitamente documentato).

---

## 10. Revisione di questo charter

Questo charter è soggetto a revisione annuale o dopo ogni evento di audit straordinario. Qualsiasi modifica richiede unanimità del Circolo e notifica pubblica con 14 giorni di preavviso.
