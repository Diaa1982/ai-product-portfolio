# API

- `GET /p17` — benchmark workbench.
- `GET /p17/config` — active configuration.
- `POST /p17/analyze` — run controlled analysis.
- `POST /p17/actions/check` — check protected decisions.
- `GET /health` — platform/config health.

The request schema is demonstrated in `synthetic/validated-benchmark-assessment.json`. Production requires authentication, authorization, rate limits, correlation IDs and approved audit storage.
