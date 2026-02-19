-- SPECULA runtime persistence schema (PostgreSQL)
-- Source: src/specula_agent/storage.py::SCHEMA_SQL

CREATE TABLE IF NOT EXISTS projects (
  project_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  current_phase TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
  artifact_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(project_id),
  phase TEXT NOT NULL,
  mode TEXT NOT NULL,
  generated_at TIMESTAMP NOT NULL,
  validated_by_human BOOLEAN NOT NULL DEFAULT false,
  payload JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS validations (
  validation_id TEXT PRIMARY KEY,
  artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
  validator_id TEXT NOT NULL,
  validator_role TEXT NOT NULL,
  decision TEXT NOT NULL CHECK (decision IN ('approve', 'reject', 'hold')),
  validated_at TIMESTAMP NOT NULL,
  validated_by_human BOOLEAN NOT NULL,
  UNIQUE (artifact_id, validator_id)
);

CREATE TABLE IF NOT EXISTS refusal_register (
  refusal_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(project_id),
  prototype_id TEXT NOT NULL,
  violated_value TEXT NOT NULL,
  opportunity_cost TEXT NOT NULL,
  identity_signal TEXT NOT NULL,
  refusal_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS guardian_reports (
  guardian_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(project_id),
  quarter TEXT NOT NULL,
  divergence_level TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  report JSONB NOT NULL,
  generated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
  event_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(project_id),
  phase TEXT,
  mode TEXT,
  event TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_artifacts_project_phase
  ON artifacts(project_id, phase);

CREATE INDEX IF NOT EXISTS idx_refusals_project_value
  ON refusal_register(project_id, violated_value);

CREATE INDEX IF NOT EXISTS idx_guardian_project_quarter
  ON guardian_reports(project_id, quarter);

CREATE INDEX IF NOT EXISTS idx_audit_project_created
  ON audit_logs(project_id, created_at);

CREATE INDEX IF NOT EXISTS idx_validations_artifact
  ON validations(artifact_id);
