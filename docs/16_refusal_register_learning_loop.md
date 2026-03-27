# Refusal Register — Learning Loop Protocol
**Version**: 1.0
**Date**: 2026-03-27
**Status**: Normative (operational protocol, integrates with orchestrator runtime)
**Repo**: specula-framework
**Dipendenza runtime**: `src/specula_agent/orchestrator.py` → `refusals_due_for_review()`

---

## 1. Scopo

Il Refusal Register è uno degli artefatti più distintivi di Specula: documentare *cosa si rifiuta* è raro nelle metodologie tradizionali. Ma nella versione precedente, il registro era un **archivio senza retroazione** — accumulava rifiuti senza che questi informassero le decisioni future.

Questo protocollo trasforma il Refusal Register da archivio a **insegnante**: ogni rifiuto registrato viene riesaminato dopo 90 giorni per verificare se il contesto è cambiato abbastanza da giustificarne la revisione.

---

## 2. Come funziona tecnicamente

### 2.1 Registrazione del rifiuto

Quando un artifact di Phase 3 in modalità `refusal_register` viene validato e avanzato, l'orchestratore salva ogni rifiuto nella chiave `refusal_learning` del `continuity_context`:

```json
{
  "refusal_learning": [
    {
      "refusal_id": "refusal-<uuid>",
      "violated_value": "radical_value_name",
      "identity_signal": "Boundary reinforced by this refusal",
      "date": "2026-03-27T00:00:00Z",
      "review_after": "2026-06-25T00:00:00Z"
    }
  ]
}
```

Il campo `review_after` è impostato automaticamente a **90 giorni** dalla data del rifiuto. Questo è il trigger della re-valutazione.

### 2.2 Query dei rifiuti maturi

Il metodo pubblico `SpeculaOrchestrator.refusals_due_for_review(reference_date)` restituisce tutti i rifiuti il cui `review_after` è passato rispetto alla data di riferimento.

Questo metodo può essere chiamato:
- Dal Guardian Loop (Phase 6) durante la revisione trimestrale
- Da qualsiasi tool esterno che monitora il progetto
- Manualmente dal Governance Architect nella quarterly review

```python
orchestrator = SpeculaOrchestrator(state)
due = orchestrator.refusals_due_for_review()
# due: lista di dict con refusal_id, violated_value, date, review_after
```

---

## 3. Il processo di re-valutazione

### 3.1 Trigger

La re-valutazione di un rifiuto viene attivata quando:
1. Il metodo `refusals_due_for_review()` restituisce entries (trigger automatico basato sul tempo)
2. Il Guardian Loop rileva segnali emergenti (`scenario_alignment.emerging`) che contraddicono o confermano il razionale originale del rifiuto
3. La community (via Phase 5) solleva esplicitamente un tema precedentemente rifiutato

### 3.2 Le domande della re-valutazione

Per ogni rifiuto in revisione, il Circolo di Sintesi (o il Governance Architect in delega) risponde a queste tre domande:

**Domanda 1 — Il contesto è cambiato?**
"Il `violated_value` che ha motivato questo rifiuto è ancora rilevante? Ci sono segnali che il contesto (mercato, tecnologia, valori sociali) lo abbia trasformato?"

**Domanda 2 — L'opportunity cost è ancora accettabile?**
"Avevamo documentato l'`opportunity_cost` di questo rifiuto. Quel costo si è materializzato? Avremmo dovuto decidere diversamente?"

**Domanda 3 — Il rifiuto ha generato un segnale di identità?**
"L'`identity_signal` documentato è stato confermato nel tempo? Il Brand ha agito coerentemente con quel segnale?"

### 3.3 Esiti possibili

| Esito | Descrizione | Azione |
|---|---|---|
| **Conferma** | Il rifiuto era corretto, il contesto non è cambiato | Aggiornare `review_after` a +90 giorni, nessuna altra azione |
| **Revisione parziale** | Il contesto è cambiato su alcuni aspetti | Aprire nuova Phase 3 su quel specifico dominio |
| **Inversione** | Il rifiuto è ora ritenuto sbagliato alla luce del contesto attuale | Re-speculation cycle obbligatorio, documentare l'inversione nel Decision Log |
| **Archiviazione** | Il tema è diventato irrilevante | Spostare l'entry in archivio, documentare il motivo |

---

## 4. Integrazione con il Guardian Loop

Il Guardian Loop (Phase 6) ha accesso al `continuity_context.refusal_learning`. Nella generazione del `guardian_report`, il Guardian deve:

1. Elencare nei `scenario_alignment.contradicting` eventuali segnali che contraddicono rifiuti precedenti
2. Elencare nei `scenario_alignment.confirming` eventuali segnali che confermano rifiuti precedenti
3. Includere in `coherence.inconsistent` eventuali comportamenti del brand che contraddicono `identity_signal` registrati nei rifiuti

In questo modo, il Refusal Register non è solo un archivio consultabile — è un **termine di paragone attivo** per la vigilanza del Guardian.

---

## 5. Formato del Decision Log per le re-valutazioni

Ogni re-valutazione produce una voce nel Decision Log con questo formato minimo:

```
[DATA] REFUSAL REVIEW — refusal_id: <id>
violated_value: <valore>
original_date: <data originale>
review_outcome: [confirm | partial_revision | inversion | archive]
rationale: <testo libero>
context_changes: <cosa è cambiato nel contesto>
reviewed_by: [ruolo1, ruolo2]
```

---

## 6. Frequenza raccomandata

- **Review automatica**: ogni volta che `refusals_due_for_review()` restituisce entries (baseline: ogni 90 giorni)
- **Review straordinaria**: quando il Guardian emette `divergence_level: critical` o `significant_drift`
- **Review programmatica**: parte obbligatoria della Brand Radar Review semestrale

---

## 7. Cosa il Learning Loop NON è

- ❌ Non è un meccanismo per "ammorbidire" i rifiuti nel tempo (il default è conferma, non inversione)
- ❌ Non è una votazione aperta: la re-valutazione è condotta dal Circolo di Sintesi, non dalla community
- ❌ Non sovrascrive il rifiuto originale: anche le inversioni vengono documentate come tali, mantenendo la traccia storica
- ✅ È uno strumento per rendere il passato un insegnante attivo, non un peso morto
