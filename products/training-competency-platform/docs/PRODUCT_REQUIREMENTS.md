# Functional requirements and end-to-end workflow

**Product lifecycle:** approved knowledge → objectives and competency targets → assessment blueprint → examiner-approved questions → learning and assessment → deterministic result → gap analysis → remediation and reassessment → evidence-linked effectiveness reporting.

## Roles
System administrator (technical configuration); knowledge owner (authoritative source approval); training manager (programmes, assignment and publication); examiner (question/rubric and review); learner (training, assessment and remediation); manager/auditor (approved analytics and evidence). The current MVP implements six selectable demo identities with a forgeable header; this is not enterprise authentication or true separation of duties.

## Executable MVP workflow
1. Knowledge owner uploads TXT, MD, searchable PDF or DOCX up to 5 MB; extracted text becomes a draft, then is approved.
2. Training manager creates a draft programme from an approved source, sets overall pass, critical threshold and max attempts, and adds ordered modules.
3. Examiner manually authors multiple-choice questions with objective and source text, flags critical questions and approves them. AI generation is not implemented.
4. Training manager publishes only after all modules have approved questions.
5. Learner enrolls, studies module content and takes its assessment; later modules remain locked until prior modules pass.
6. Backend validates every answer, calculates total and critical-control percentages, stores attempt and question snapshot, and reports source-linked gaps.
7. Pass requires BOTH score thresholds. Failed learners can retry within the configured limit; successful learners unlock the next module. Audit events are stored in the database.

## Functional requirement groups
| Group | Executable now | Target extension |
|---|---|---|
| Identity and permissions | Six demo roles and endpoint checks | OIDC, RBAC and organization scoping |
| Knowledge | Extract, draft, approve | Immutable source versions, metadata, RAG |
| Programme | Draft, modules, publish | Versioned objectives and competencies |
| Assessment | Manual MCQ, approval, thresholds | Blueprint, cognitive levels, AI question generation, rubrics |
| Delivery | Enrollment, exam, sequential gate | Assignment, resource progress, autosave and timers |
| Evaluation | Objective MCQ, critical score, attempts | Narrative evaluation and human grading |
| Improvement | Objective/source gap feedback | Tracked remediation and gap closure |
| Reporting | Learner results and basic audit | Cohort, retention and qualified impact analytics |

**Acceptance:** seeded learner cannot open module 2 initially; wrong critical answer fails and blocks progression; correct reassessment passes and unlocks module 2; exam API does not expose answer key. This package's workflow test was run locally and passed (one test).