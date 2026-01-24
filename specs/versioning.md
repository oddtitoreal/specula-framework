# Versioning policy

## Documents
- Normative documents (Foundations, Constitution, Governance, Control Logic, Schemas) use **SemVer**: `MAJOR.MINOR`.
  - MAJOR: breaking conceptual/governance change
  - MINOR: additive clarifications, non-breaking changes

## Playbooks and prompts
- Use `MAJOR.MINOR.PATCH`.
  - PATCH: prompt wording improvements with unchanged behavior
  - MINOR: new prompts/templates
  - MAJOR: behavioral changes (e.g., routing, refusal rules)

## Change control
- Every change requires:
  - update to the document header (version/date)
  - entry in `CHANGELOG.md`
  - PR review by at least 1 owner (2 for normative docs)
