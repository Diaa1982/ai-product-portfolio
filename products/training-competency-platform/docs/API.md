# MVP API reference

Base URL `/api`. Interactive OpenAPI: `/docs`. Role-protected routes use `X-Demo-User: <uuid>` from `GET /api/users`. **This is an insecure demo-only header, not authentication.**

| Method | Endpoint | Role / effect |
|---|---|---|
| GET | `/users` | List synthetic demo identities |
| GET | `/documents` | List documents |
| POST | `/documents/upload` | Knowledge owner/admin: multipart file and title; creates draft |
| POST | `/documents/{id}/approve` | Knowledge owner/admin: approve |
| GET/POST | `/programmes` | List / manager creates draft from approved document |
| GET | `/programmes/{id}` | Programme and ordered modules |
| POST | `/programmes/{id}/modules` | Manager adds module to draft |
| GET/POST | `/modules/{id}/questions` | Examiner/manager reads; examiner creates draft |
| POST | `/questions/{id}/approve` | Examiner/admin approves |
| POST | `/programmes/{id}/publish` | Manager/admin publishes when ready |
| POST | `/programmes/{id}/enroll` | Learner enrolls |
| GET | `/enrollments/{eid}/modules/{mid}/exam` | Learner obtains exam without answer key |
| POST | `/enrollments/{eid}/modules/{mid}/submit` | Learner submits `{"answers":{"question-uuid":0}}`; receives scores and gaps |
| GET | `/my-results` | Learner's attempt history |
| GET | `/audit` | Auditor/admin latest 100 audit events |
| GET | `/health` | Basic health response |

Typical status codes: 401 unknown demo identity; 403 wrong role, locked module or attempts exhausted; 404 missing resource; 409 invalid draft/published transition; 422 invalid answers or publication prerequisites. The API does not provide production session, organization tenancy, versioned rubrics, asynchronous ingestion or AI generation yet.