"""Persistence adapters for project state, artifacts, and audit events."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from textwrap import dedent
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .orchestrator import ProjectState

SCHEMA_SQL = dedent(
    """
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
    """
).strip()


class StorageError(RuntimeError):
    """Raised when persistence operations fail."""


class StorageAdapter:
    """No-op adapter used when DB persistence is disabled."""

    def init_schema(self) -> None:
        return

    def upsert_project_state(self, state: ProjectState) -> None:
        return

    def insert_artifact(self, project_id: str, artifact: Dict[str, Any]) -> None:
        return

    def insert_validation(
        self,
        artifact_id: str,
        *,
        validated_by_human: bool,
        validator_id: str,
        validator_role: str,
        decision: str,
    ) -> None:
        return

    def get_validations(self, artifact_id: str) -> List[Dict[str, Any]]:
        return []

    def append_audit(
        self,
        *,
        project_id: str,
        phase: Optional[str],
        mode: Optional[str],
        event: str,
        content: str,
    ) -> None:
        return


@dataclass
class PostgresStorage(StorageAdapter):
    """PostgreSQL adapter for runtime persistence."""

    database_url: str

    def __post_init__(self) -> None:
        try:
            import psycopg  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise StorageError(
                "psycopg is required for --database-url usage. Install with `pip install psycopg[binary]`."
            ) from exc
        self._psycopg = psycopg

    @staticmethod
    def _utc_now() -> datetime:
        return datetime.now(timezone.utc).replace(microsecond=0)

    def _connect(self):
        return self._psycopg.connect(self.database_url)

    def init_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)

    def upsert_project_state(self, state: ProjectState) -> None:
        now = self._utc_now()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO projects (project_id, name, current_phase, created_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (project_id)
                    DO UPDATE SET current_phase = EXCLUDED.current_phase
                    """,
                    (state.project_id, state.project_id, state.current_phase, now),
                )

    def insert_artifact(self, project_id: str, artifact: Dict[str, Any]) -> None:
        meta = artifact["meta"]
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO artifacts
                      (artifact_id, project_id, phase, mode, generated_at, validated_by_human, payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                    ON CONFLICT (artifact_id) DO NOTHING
                    """,
                    (
                        meta["artifact_id"],
                        project_id,
                        str(meta["phase"]),
                        meta["mode"],
                        meta["generated_at"],
                        bool(meta["validated_by_human"]),
                        json.dumps(artifact["payload"]),
                    ),
                )

    def insert_validation(
        self,
        artifact_id: str,
        *,
        validated_by_human: bool,
        validator_id: str,
        validator_role: str,
        decision: str,
    ) -> None:
        decision_key = decision.lower().strip()
        if decision_key not in {"approve", "reject", "hold"}:
            raise StorageError("decision must be approve, reject, or hold")
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO validations
                      (validation_id, artifact_id, validator_id, validator_role, decision, validated_at, validated_by_human)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (artifact_id, validator_id) DO NOTHING
                    """,
                    (
                        str(uuid4()),
                        artifact_id,
                        validator_id,
                        validator_role,
                        decision_key,
                        self._utc_now(),
                        validated_by_human,
                    ),
                )
                if cur.rowcount == 0:
                    raise StorageError(
                        f"duplicate validator signature for artifact `{artifact_id}` and validator `{validator_id}`"
                    )

    def get_validations(self, artifact_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT validator_id, validator_role, decision, validated_by_human, validated_at
                    FROM validations
                    WHERE artifact_id = %s
                    ORDER BY validated_at ASC
                    """,
                    (artifact_id,),
                )
                rows = cur.fetchall()
        return [
            {
                "validator_id": row[0],
                "validator_role": row[1],
                "decision": row[2],
                "validated_by_human": bool(row[3]),
                "validated_at": row[4].isoformat() if hasattr(row[4], "isoformat") else str(row[4]),
            }
            for row in rows
        ]

    def append_audit(
        self,
        *,
        project_id: str,
        phase: Optional[str],
        mode: Optional[str],
        event: str,
        content: str,
    ) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO audit_logs (event_id, project_id, phase, mode, event, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (str(uuid4()), project_id, phase, mode, event, content, self._utc_now()),
                )


def build_storage(database_url: str | None) -> StorageAdapter:
    """Factory for storage adapter."""
    if not database_url:
        return StorageAdapter()
    return PostgresStorage(database_url=database_url)
