# API

OpenAPI is available at `/docs` when the service runs.

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Service and config version |
| GET | `/p01` | PFM Agent Command Center |
| GET | `/p01/config` | Versioned agents, transitions and controls |
| POST | `/p01/analyze` | Validate, calculate, classify and evaluate handoff |
| POST | `/p01/actions/check` | Deny protected autonomous actions |
| POST | `/p01/handoffs/approve` | Record a configured human workflow decision |

Example action check:

```json
{"action":"authorize payment"}
```

The result must be `DENY_AUTONOMOUS_EXECUTION`. Production requires authentication, authorization, idempotency, schema/version controls, rate limits, evidence-store integration and tamper-evident audit persistence.
