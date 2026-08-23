# API

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Service and configuration status |
| GET | `/p02` | Fiscal Intelligence Workbench |
| GET | `/p02/config` | Synthetic profile, rules and acceptance themes |
| POST | `/p02/analyze` | Validate, calculate, reconcile, classify and gate a fiscal snapshot |
| POST | `/p02/dataset/readiness` | Check domain load order and completeness |

OpenAPI is available at `/docs`. Production requires authenticated service identities, RBAC/SoD, schema registry, idempotency, pagination/batching, data contracts, approval/evidence store integration, rate limiting, observability and controlled API/version retirement.
