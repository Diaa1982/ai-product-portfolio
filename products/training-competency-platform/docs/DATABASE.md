# Database: executable schema and enterprise target

The runnable MVP uses SQLAlchemy models in `app/main.py` and `Base.metadata.create_all`. PostgreSQL 16 is used with Compose; SQLite is an optional local/test backend. No Alembic migrations are included.

| Implemented table | Principal fields and relationships |
|---|---|
| `users` | UUID string PK, name, role |
| `documents` | UUID string PK, owner_id FK users, title, integer version, extracted text, SHA-256, status, created_at |
| `programmes` | UUID string PK, document_id FK, name, description, status, pass_pct, critical_pct, max_attempts |
| `modules` | UUID string PK, programme_id FK, title, sequence, content; unique (programme_id, sequence) |
| `questions` | UUID string PK, module_id FK, prompt, JSON options, correct_index, objective string, critical boolean, source string, status, version |
| `enrollments` | UUID string PK, learner_id FK, programme_id FK; unique (learner_id, programme_id) |
| `attempts` | UUID string PK, enrollment_id FK, module_id FK, attempt_number, JSON answers and question_snapshot, total/critical scores, passed, created_at; unique (enrollment_id,module_id,attempt_number) |
| `audit_events` | UUID string PK, actor_id FK, action, entity_type, entity_id, JSON details, timestamp |

The eight-table implementation is intentionally smaller than the target schema. Target domains: identity (organizations, organizational_units, users, roles and permissions); knowledge (collections, documents, document_versions, chunks and ingestion jobs); learning (programme versions, modules, objectives and resources); competency (competencies, levels and requirements); assessment (assessment/question versions, options, rubrics, scoring policies); delivery (enrollments, attempts and responses); evaluation (scores/results); improvement (gaps/remediation); analytics (metrics/observations); AI (models/prompts/executions/sources); governance (approvals/audit).

**Target integrity:** UUID PK/FKs, TIMESTAMPTZ, CHECK bounds for scores, immutable published versions, source and scoring-policy snapshot per attempt, unique attempt numbering under transactional locking, scoped foreign keys/RLS, BTREE FK/report indexes, appropriate GIN/pgvector indexes and independent append-only audit export. None of these target-only controls should be represented as already implemented.