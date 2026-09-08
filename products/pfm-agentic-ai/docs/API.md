# API

The product container now starts the P01 management-demo service. OpenAPI is available at `/docs`.

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Demo service health and mode |
| GET | `/` | Astra-style management demonstration |
| GET | `/command-center` | Configurable agent command-center prototype |
| GET | `/api/config` | Versioned PFM agent mandates and human gates |
| GET | `/api/signals` | Retrieve authoritative public signals with provenance/status |
| GET | `/api/fiscal` | Current coherent synthetic fiscal state |
| GET | `/api/agents` | Agent registry plus current synthetic runtime events |
| POST | `/api/scenario` | Apply a controlled synthetic fiscal scenario |
| POST | `/api/reset` | Restore the synthetic baseline |
| POST | `/api/ask` | Ask governed executive questions over the synthetic fiscal state |
| POST | `/api/reports` | Generate variable evidence-labelled management-demo reports |

Example scenario:

```json
{"scenario":"cash_pressure"}
```

Supported scenarios are `baseline`, `revenue_shock`, `capital_delay`, `cash_pressure`, and `close_exception`.

Example Ask PFM request:

```json
{"question":"Show delayed projects with high cash requests"}
```

Example report request:

```json
{
  "report_type":"Fiscal Risk",
  "entity_id":"C",
  "mandate":"Treasury",
  "period":"Year to date",
  "include_forecast":true,
  "include_delays":true,
  "include_exceptions":true,
  "include_evidence":true
}
```

The original governed P01 orchestration module remains in the repository and continues to deny autonomous protected financial actions in its unit tests. The management-demo API does not expose transaction execution endpoints.

Production requires authentication, authorization, valid organizational delegations, segregation of duties, idempotency, source-system contracts, evidence/audit persistence, rate limits, monitoring and formal go-live approval.
