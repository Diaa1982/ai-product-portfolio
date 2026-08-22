# API

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Service/configuration status |
| GET | `/p12` | Revenue Reconciliation Workbench |
| GET | `/p12/config` | Forms, source reports, rules and boundaries |
| POST | `/p12/reconcile` | Calculate, match, reconcile and route exceptions |
| POST | `/p12/actions/check` | Deny protected autonomous actions |

OpenAPI is at `/docs`. Production requires SSO/RBAC/SoD, source/bank/treasury contracts, secure file intake, idempotency, rule/effective-date versioning, evidence/exception/approval stores, batching, observability and controlled API retirement.
