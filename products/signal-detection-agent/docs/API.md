# API

| Method | Path | Purpose |
|---|---|---|
| GET | `/p04` | Detection interface |
| GET | `/p04/config` | Active source/scoring configuration |
| GET | `/p04/sources` | Synthetic approved-source view |
| POST | `/p04/detect` | Verify, detect, score and route candidate |
| POST | `/p04/approve` | Record protected publication decision |
| GET | `/health` | Service/config health |
| GET | `/docs` | OpenAPI explorer |

A complete request is in `../synthetic/verified-change.json`. Production roles must come from signed enterprise identity claims, not request text.
