# API

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Service/configuration status |
| GET | `/p11` | Accounting Review Workbench |
| GET | `/p11/config` | Controlled review types, thresholds and boundaries |
| POST | `/p11/review` | Run journal, reconciliation or disclosure exception review |
| POST | `/p11/actions/check` | Deny protected autonomous accounting actions |

OpenAPI is available at `/docs`. Production requires SSO/RBAC/SoD, controlled file scanning/extraction, schema/version contracts, idempotency, evidence and approval stores, knowledge retrieval with citations, rate limits and audit/monitoring integration.
