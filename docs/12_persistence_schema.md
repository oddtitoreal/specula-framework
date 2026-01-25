# SPECULA AI – PERSISTENCE SCHEMA (MVP)

Version: 1.0
Date: 2026-01-24

This document specifies a minimal persistence model for Refusal Register
and Guardian outputs, plus supporting tables.

---

## 1. Tables (SQL Sketch)

```sql
CREATE TABLE projects (
  project_id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  current_phase TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE artifacts (
  artifact_id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(project_id),
  phase TEXT NOT NULL,
  mode TEXT NOT NULL,
  generated_at TIMESTAMP NOT NULL,
  validated_by_human BOOLEAN NOT NULL DEFAULT false,
  payload JSONB NOT NULL
);

CREATE TABLE validations (
  validation_id UUID PRIMARY KEY,
  artifact_id UUID NOT NULL REFERENCES artifacts(artifact_id),
  validator_id TEXT NOT NULL,
  validated_at TIMESTAMP NOT NULL,
  validated_by_human BOOLEAN NOT NULL
);

CREATE TABLE refusal_register (
  refusal_id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(project_id),
  prototype_id UUID NOT NULL,
  violated_value TEXT NOT NULL,
  opportunity_cost TEXT NOT NULL,
  identity_signal TEXT NOT NULL,
  refusal_date TIMESTAMP NOT NULL
);

CREATE TABLE guardian_reports (
  guardian_id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(project_id),
  quarter TEXT NOT NULL,
  divergence_level TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  report JSONB NOT NULL,
  generated_at TIMESTAMP NOT NULL
);
```

---

## 2. Indexes

```sql
CREATE INDEX idx_artifacts_project_phase
  ON artifacts(project_id, phase);

CREATE INDEX idx_refusals_project_value
  ON refusal_register(project_id, violated_value);

CREATE INDEX idx_guardian_project_quarter
  ON guardian_reports(project_id, quarter);
```

---

## 3. Queries (Operational)

### Q1: Retrieve active Refusal Register for a project
```sql
SELECT *
FROM refusal_register
WHERE project_id = :project_id
ORDER BY refusal_date DESC;
```

### Q2: Check if a proposed prototype conflicts with past refusals
```sql
SELECT *
FROM refusal_register
WHERE project_id = :project_id
  AND violated_value = :candidate_value;
```

### Q3: Latest validated artifact per phase
```sql
SELECT DISTINCT ON (phase) *
FROM artifacts
WHERE project_id = :project_id
  AND validated_by_human = true
ORDER BY phase, generated_at DESC;
```

### Q4: Guardian trend over time
```sql
SELECT quarter, divergence_level, recommended_action
FROM guardian_reports
WHERE project_id = :project_id
ORDER BY quarter ASC;
```

---

## 4. Immutability Rules

- `refusal_register` entries are append-only.
- `guardian_reports` entries are append-only.
- Edits require a new artifact with a pointer to the previous record.
