# Technical architecture and build specification

## Runnable local MVP
Browser → same-origin HTML/CSS/JS at `web/index.html` → FastAPI `app/main.py` → SQLAlchemy → PostgreSQL 16 (or local SQLite). Docker Compose provisions `db` and `app`; database health precedes application startup. `app/seed.py` creates tables and synthetic data on first run. PostgreSQL data persists in `pgdata`.

## Enterprise target (not yet built)
React/Next.js TypeScript role-based frontend → FastAPI modular services for knowledge, training, assessment, delivery, evaluation, improvement, reporting and governance → PostgreSQL with normalized domains/pgvector → S3-compatible object storage and asynchronous ingestion queue → controlled AI gateway and model/prompt registry. OIDC/SSO, RBAC, tenant isolation, audit export, encryption, observability and migrations are mandatory before real deployment.

## AI agent contracts
Knowledge ingestion agent extracts/structures/chunks approved references. Training designer proposes objectives. Question generator produces source-cited drafts and rubrics. Narrative evaluator proposes criterion marks. Gap agent maps errors to objectives. Recommendation agent proposes targeted learning. Reporting agent summarizes evidence with explicit limitations. Humans approve sources, assessment publication and material grading decisions. Deterministic backend owns pass/fail and progression.

## Build order
1. Secure identity, scoped permissions, Alembic migrations and audit controls.
2. Immutable approved source versions, object storage and evidence retrieval.
3. Versioned programme/objective/competency model and assignments.
4. Question bank, examiner review, scoring-policy snapshots and concurrency-safe attempts.
5. AI generation and narrative evaluation with human approval.
6. Remediation, analytics, localization, accessibility, tests and secured deployment.

## Validation
No answer key in learner exam API; critical-control failure blocks progression even with a sufficient overall score; source/rubric/policy versions persist with attempts; unauthorized actors cannot modify approvals or records; historical decisions remain traceable; backup/restore and migration tests pass.