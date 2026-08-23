# API

- `GET /p18` — assessment workbench.
- `GET /p18/config` — active scheme configuration.
- `POST /p18/assess` — evidence-led assessment.
- `POST /p18/actions/check` — protected-action check.
- `GET /health` — platform/config health.

The request schema is in `synthetic/moderation-ready-assessment.json`. Production requires authenticated identities, role authorization, rate limits, signed decisions and approved audit storage.
