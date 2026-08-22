# API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/p05` | Guided Service Design Studio |
| GET | `/p05/config` | Versioned methodology and controls |
| POST | `/p05/design` | Generate classification, service card, journey, blueprint, methods, gate evaluation and report |
| POST | `/p05/actions/check` | Check if an action requires accountable human authority |

Use `synthetic/complete-g2g-service.json` as the request body. Validation failures return HTTP 400; out-of-profile direct-individual service requests are rejected. OpenAPI is at `/docs`.
