# API

- `GET /p16` — dashboard.
- `GET /p16/config` — active non-secret configuration.
- `POST /p16/analyze` — validate and analyze an `ITManagementInput` payload.
- `POST /p16/actions/check` — determine whether an action is protected.
- `GET /health` — service and configuration health.

Errors use HTTP 400 for invalid input and 403 for prohibited operations where applicable. Production must add authenticated identities, role/purpose authorization, request limits, correlation IDs, schema versioning and immutable audit storage. API output is decision support, not approval.
