# SPECULA Version Map

## Purpose

This document clarifies version tracks across the SPECULA repository ecosystem.

## Current Snapshot (2026-10-21)

| Repository | Track | Current reference | Notes |
|---|---|---|---|
| `specula-framework` | Framework/runtime track | 1.3.0 | Canonical runtime/spec track; schemas `phase0` to `phase6`, `decision_log`, `preferable_future` |
| `specula-method` | Public method track | 2.0.0 | Six-phase canonical sequence, DNA produced by the Value Stress Test after the scenarios |
| `specula-bos` | Product architecture track | 2.2.0 | Seven layers, workshops, Memory Architecture, Circle |
| `specula-skill` | Implementation skill track | 0.3.0 | Constitution and state-machine governance; criteria as hypotheses |
| `specula-handbook` | Handbook track (date-based) | 2026.11 | Italian handbook at docs.specula.design; documents the versions above |

## Interpretation

- Tracks are related but not numerically identical.
- `specula-framework` version references describe canonical governance/runtime evolution.
- `specula-method`, `specula-bos` and `specula-skill` evolve independently while mapping to framework semantics.
- The method phase numbers (`0`, `1`, `1.5`, `2` to `6`) are the same in `specula-method`, `specula-bos`, the handbook and the framework schemas.

## Linking Rule

When documenting versions in non-framework repositories:
1. State local repository version.
2. Reference relevant framework version semantics explicitly.
3. Avoid implying that track numbers are interchangeable.

## Governance

For versioning policy details, see:
- `specs/versioning.md` (framework policy)
- `CHANGELOG.md` in each repository
