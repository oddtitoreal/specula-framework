# SPECULA AI – VALIDATION TESTS (MVP)

Version: 1.0
Date: 2026-01-24

This document defines minimal automated tests to enforce non-oracularity
and output format constraints.

---

## 1. Schema and Meta Tests

### T1: JSON Schema Validation
Input: AI output JSON
Pass if: validates against phase schema and common meta schema.

### T2: Phase Consistency
Pass if: `meta.phase` == orchestrator `current_phase`.

### T3: Mode Enum
Pass if: `meta.mode` in canonical list (see `specs/terminology.md`).

### T4: Human Validation Default
Pass if: `meta.validated_by_human == false` on new artifacts.

---

## 2. Non-Oracularity Tests

### T5: Forbidden Decision Fields
Fail if: output contains `decision: true` or `decision=true`.

### T6: Prescriptive Language (Heuristic)
Fail if: output contains phrases like:
- "you should"
- "the best choice"
- "the correct option"
- "we recommend"
- "choose X"

### T7: Ranking-as-Decision
Fail if: output includes ordered rankings with directives:
- "1) X 2) Y 3) Z and choose 1"

---

## 3. One-Question Rule

### T8: Exactly One Question
Pass if: the assistant text contains exactly one "?".
Fail if: zero or more than one "?".

---

## 4. Output Envelope

### T9: MODE | PHASE Header
Pass if: first line matches `MODE: <mode> | PHASE: <phase>`.

### T10: Max Lines Before Question
Pass if: no more than 6 lines before the question line.

---

## 5. Remediation Rules

If any test fails:
1) Trigger `slowdown` or `refusal` mode.
2) Ask for human clarification.
3) Re-run after human input.
