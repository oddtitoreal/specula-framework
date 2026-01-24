# SPECULA AI – CONTROL LOGIC AND STATE MACHINE

This document defines the **control logic**, **state machine**, and **governance rules** that regulate how SPECULA AI operates across phases.

It specifies **when** the system can advance, **when it must stop**, and **when human intervention is mandatory**.

This document is **normative**.

It complements:

* *SPECULA AI – JSON Schemas and Output Architecture*
* *SPECULA AI – System Architecture and Input Specifications*

In case of conflict:

1. **Control Logic overrides Process Descriptions**
2. **Output Schemas override everything else**

---

## 1. SPECULA AS A CONTROLLED COGNITIVE SYSTEM

SPECULA is **not** a linear pipeline.

It is a **phase-governed cognitive system** with:

* explicit state transitions
* hard validation gates
* enforced non-oracular behavior
* mandatory human-in-the-loop checkpoints

The system is designed to **prevent premature convergence**, **ethical drift**, and **automation of judgment**.

---

## 2. GLOBAL STATE MACHINE

### Allowed Phases

```text
PHASE 0  → Activation
PHASE 1  → Speculative Scenarios
PHASE 1.5→ Competitive Futures Map
PHASE 2  → Brand Archaeology (DNA)
PHASE 3  → Prototyping + Ethical Gate
PHASE 4  → Narrative System
PHASE 5  → Community Co‑Creation
PHASE 6  → Guardian Monitoring
```

### Allowed Transitions (Default)

```text
0 → 1
1 → 1.5
1.5 → 2
2 → 3
3 → 4
4 → 5
5 → 6
6 → 1   (Re‑Speculation Loop)
```

### Forbidden Transitions (Hard Rules)

```text
1 → 3   (No prototyping without DNA)
2 → 4   (No narrative without ethical validation)
3 → 5   (No co‑creation on invalidated prototypes)
ANY → ANY (if validation == false)
```

---

## 3. PHASE ENTRY CONDITIONS

Each phase can be entered **only if all entry conditions are satisfied**.

### Example – Phase 3 Entry

Phase 3 (Prototyping) can start **only if**:

* Phase 1 scenarios exist and are human‑validated
* Phase 2 Brand DNA exists and is validated
* `validated_by_human == true` for both artifacts

If conditions are not met → **SYSTEM HALT**

---

## 4. HUMAN VALIDATION GATES (MANDATORY)

Human validation is **not optional**.

### Validation‑Required Phases

| Phase | Validation Required | Scope                       |
| ----- | ------------------- | --------------------------- |
| 1     | YES                 | Scenarios selection         |
| 2     | YES                 | Brand DNA confirmation      |
| 3     | YES                 | Ethical Gate decisions      |
| 4     | YES                 | Meta‑narrative approval     |
| 5     | YES                 | Accepted / rejected changes |
| 6     | YES                 | Guardian interpretation     |

### Enforcement Rule

```text
If validated_by_human == false
→ phase cannot advance
→ outputs are marked “non‑operational”
```

---

## 5. NON‑ORACULAR ENFORCEMENT

SPECULA **must never make decisions**.

### Forbidden Output Patterns

* `decision: true`
* “You should choose…”
* “The correct option is…”

### Mandatory Patterns

* Questions
* Alternatives
* Trade‑offs
* Explicit uncertainty

If oracular language is detected → **REWRITE OUTPUT**

---

## 6. ETHICAL GATE CONTROL (PHASE 3)

The Ethical Gate is a **blocking control mechanism**.

### Ethical Gate Outcomes

| Status | System Behavior                            |
| ------ | ------------------------------------------ |
| PASS   | Prototype eligible for narrative synthesis |
| HOLD   | Requires human clarification / redesign    |
| FAIL   | Prototype rejected + logged in Registry    |

### Hard Rule

```text
FAIL prototypes can NEVER re‑enter the pipeline
unless explicitly re‑speculated in Phase 1
```

---

## 7. REFUSAL REGISTRY AS IDENTITY MEMORY

The Registry of Refusals is a **persistent identity constraint**.

### Rules

* Refusals are immutable
* They constrain future generations
* Guardian must check new actions against past refusals

If a future action violates a registered refusal → **ALERT + ESCALATION**

---

## 8. GUARDIAN DIVERGENCE LOGIC (PHASE 6)

### Divergence Classification

| Level   | Meaning                  | System Action          |
| ------- | ------------------------ | ---------------------- |
| Noise   | Minor fluctuation        | Monitor                |
| Drift   | Directional misalignment | Correct                |
| Rupture | Structural incoherence   | Trigger Re‑Speculation |

### Rupture Rule

```text
If divergence == rupture
→ Phase reset to Phase 1
→ Guardian opens new speculative cycle
```

---

## 9. RE‑SPECULATION LOOP

Re‑speculation is **not failure**.

It is a **designed regenerative mechanism**.

### Trigger Conditions

* Guardian detects rupture
* Brand behavior violates refusal registry
* External shock invalidates core assumptions

### Loop Behavior

```text
Phase 6 → Phase 1
Preserve: DNA, Refusals
Re‑generate: Scenarios, Prototypes, Narrative
```

---

## 10. FAILURE MODES AND SAFE STOPS

### Hard Stop Conditions

* Missing validation
* Ethical Gate failure
* Contradiction between actions and DNA

### System Response

* Stop progression
* Surface contradiction explicitly
* Ask for human decision

---

## 11. SUMMARY: WHAT THIS LOGIC PREVENTS

This control logic ensures SPECULA:

* Never automates judgment
* Never optimizes away ethics
* Never converges prematurely
* Never forgets past refusals
* Never confuses intelligence with authority

---

**SPECULA AI – Control Logic and State Machine**
Version 1.0
