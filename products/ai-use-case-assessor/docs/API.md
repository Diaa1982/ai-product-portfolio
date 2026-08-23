# API

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service and P08 configuration health |
| GET | `/p08` | Dedicated assessment interface |
| GET | `/p08/config` | Active versioned scoring configuration |
| POST | `/p08/assess` | Validate and score an intake |
| POST | `/p08/approve` | Record a protected CEO decision |
| GET | `/docs` | OpenAPI explorer |

`POST /p08/assess` accepts the structure documented in [DATA-MODEL.md](DATA-MODEL.md); a complete synthetic request is in `../synthetic/complete-assessment.json`.

`POST /p08/approve` requires `assessment_id`, a supported protected `action`, `approver_role: CEO`, `decision` (`approved`, `rejected` or `returned`) and a reason. The candidate enforces role text; production must bind it to authenticated enterprise identity.

Errors use standard FastAPI JSON. Invalid input is 400/422; protected approval by another role is 403.
