# SPECULA Version Map

## Purpose

This document clarifies version tracks across the SPECULA repository ecosystem.

## Current Snapshot (2026-03-20)

| Repository | Track | Current reference | Notes |
|---|---|---|---|
| `specula-framework` | Framework/runtime track | v2.3 references + v2.4.5.x aligned proposal | Canonical runtime/spec track |
| `specula-method` | Public method track | v1.x | Open method evolution track |
| `specula-skill` | Implementation skill track | v0.1.x | Technical subset focused on constitution/state-machine governance |

## Interpretation

- Tracks are related but not numerically identical.
- `specula-framework` version references describe canonical governance/runtime evolution.
- `specula-method` and `specula-skill` evolve independently while mapping to framework semantics.

## Linking Rule

When documenting versions in non-framework repositories:
1. State local repository version.
2. Reference relevant framework version semantics explicitly.
3. Avoid implying that track numbers are interchangeable.

## Governance

For versioning policy details, see:
- `specs/versioning.md` (framework policy)
- `CHANGELOG.md` in each repository
