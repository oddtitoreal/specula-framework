# Alignment and Document Ownership

## Purpose

This file defines ownership and synchronization rules across the SPECULA repositories.

Related repositories:
- `specula-framework` (this repo)
- `specula-method`: <https://github.com/oddtitoreal/specula-method>
- `specula-skill`: <https://github.com/oddtitoreal/specula-skill>

## Ownership Matrix

| Content type | Canonical owner | Notes |
|---|---|---|
| Governance specs (`specs/`) | `specula-framework` | Source of truth for precedence, terminology, versioning policy |
| Runtime schemas (`schemas/`) | `specula-framework` | Source of truth for runtime contracts |
| Runtime implementation (`src/`) | `specula-framework` | Source of truth for executable runtime behavior |
| Strategic method narrative (open profile) | `specula-method` | Public method documentation and facilitation profile |
| Constitution/state-machine implementation subset | `specula-skill` | Technical subset for governance implementation examples |

## Synchronization Rules

1. Terminology changes in `specula-framework/specs/terminology.md` must be reflected in:
   - `specula-method` runtime alignment docs (if impacted)
   - `specula-skill` alignment/boundary docs (if impacted)
2. Runtime schema changes in `specula-framework/schemas/` must update corresponding references in:
   - `specula-method/docs/runtime-alignment.md`
   - `specula-skill/ALIGNMENT.md` (boundary/mapping section)
3. Method-level narrative changes in `specula-method` should be consumed by reference, not by silent copy.
4. `specula-skill` may keep local convenience docs, but canonical ownership must be declared.

## Practical Rule: Prefer Linking Over Copying

- Link to canonical documents across repos when possible.
- If content is copied for convenience, include a note indicating canonical owner.

## Validation Checklist for Cross-Repo PRs

- Are ecosystem links still valid?
- Are version references still consistent?
- Are ownership boundaries still accurate?
- Were affected alignment files updated?
