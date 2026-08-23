# API

- `GET /p15` — architecture workbench.
- `GET /p15/config` — active metamodel.
- `POST /p15/analyze` — repository/impact/rationalization analysis.
- `POST /p15/changes/classify` — governance route.
- `POST /p15/actions/check` — protected decision check.
- `GET /health` — health/config version.

The request schema is shown in `synthetic/connected-enterprise-model.json`. Production requires authenticated identities, authorization, request limits and approved audit storage.
