# API

- `GET /p13` — workbench.
- `GET /p13/config` — active configuration.
- `POST /p13/analyze` — assess architecture.
- `POST /p13/actions/check` — test protected action.
- `GET /health` — health and config version.

The analyze schema is demonstrated in `synthetic/complete-pfm-architecture.json`. Production needs authenticated identities, authorization, rate limits, correlation IDs and approved audit storage.
