# Training, Assessment & Competency Management Platform

## Status
Specification and interactive prototype. Not a deployed production system.

## Product objective
An auditable training lifecycle: approved knowledge → learning objectives and competency requirements → examiner-configured assessment blueprint → source-grounded question generation and approval → learner delivery → deterministic pass/fail and progression → rubric-based evaluation → gap analysis → remediation → reassessment → impact measurement.

## User roles
System Administrator, Knowledge Owner, Training Manager, Examiner, Learner, Management/Auditor. Distinguish content preparation from approval; technical roles do not approve business content.

## MVP workflow
1. Ingest and version documents with owner, classification, effective date and approval metadata. Only approved effective versions are eligible for published assessments.
2. Create programme, modules, resources, learning objectives and competency targets.
3. Examiner configures question types, cognitive distribution, pass thresholds, critical-control minimum, attempts and mandatory questions.
4. Generate questions with source chunk citations and rubric; examiner reviews and approves before publication.
5. Learner completes gated modules and assessment. Save the exact version and randomized presentation order.
6. Objective answers are graded deterministically; narrative answers receive rubric-based AI proposals with human review where configured.
7. Rules engine finalizes pass/fail, remediation, progression and reassessment eligibility.
8. Analytics report knowledge gain, objective achievement, gaps, retention and carefully qualified operational KPI comparisons.

## Core decision rules
A final result requires complete submission and any mandatory review. Pass only when overall score >= configured pass mark, critical question score >= critical minimum and all mandatory requirements are met. Attempts and progression are enforced by versioned application rules, not LLM discretion. Any authorized override requires justification and audit evidence.

## Architecture
Next.js/React TypeScript frontend; FastAPI modular backend; PostgreSQL and pgvector; Redis/Celery jobs; S3-compatible object storage; OIDC SSO; provider-independent AI gateway. Keep deterministic scoring outside AI, with approved model/prompt versions, retrieval evidence, structured evaluations and immutable publication snapshots.

## Relational domains
identity: organizations, organizational_units, users, roles, permissions, role_permissions, user_roles.
knowledge: collections, documents, document_versions, collection_documents, document_chunks, ingestion_jobs.
learning: programmes, programme_versions, modules, learning_objectives, learning_resources.
competency: competencies, competency_levels, objective_competencies, role_requirements.
assessment: assessments, assessment_versions, question_bank, question_versions, question_options, question_objectives, question_sources, rubrics, rubric_criteria, assessment_questions, scoring_policies.
delivery: enrollments, module_progress, resource_progress, assessment_attempts, attempt_questions, responses.
evaluation: evaluation_records, criterion_scores, assessment_results, objective_results, competency_results.
improvement: learning_gaps, recommendations, remediation_plans, remediation_actions.
analytics: training_metrics, metric_observations, training_efficiency.
ai: model_registry, prompt_versions, executions, execution_sources.
governance: approval_requests, approval_decisions, audit_events.

## Database rules
UUID primary keys; explicit foreign keys; TIMESTAMPTZ; JSONB only for validated flexible configuration; score and percentage checks; organization isolation; immutable approved versions; append-only audit and approval decisions; unique attempt numbers and version uniqueness; B-tree transaction indexes, GIN search and HNSW embeddings. Preserve document, rubric, question, assessment and scoring-policy versions for every attempt.

## Screens
Dashboard; Knowledge Repository; Programme Builder; Objectives and Competencies; Assessment Designer; Question Review; Learner Portal; Assessment Player; Results; Gap Analysis and Remediation; Management Analytics; Audit and Approvals.

## MVP acceptance scenario
Using synthetic budget-control materials, approve a source and five questions, set an 80% pass mark and 80% critical minimum, take an assessment, block progression when the critical rule fails, inspect objective gaps, remediate and reassess. Verify source/version/rule/response/evaluation provenance. A browser-only prototype is not evidence of enterprise authentication, server audit, ingestion or AI correctness.

## Implementation status
The full enterprise backend, live RAG, PostgreSQL migrations, OIDC, persistence, and deployment are not yet implemented. Do not upload confidential organization documents into a browser-only demo or publish a public Pages site containing internal data.
