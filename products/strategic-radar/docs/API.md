# API

| Method | Path | Purpose |
|---|---|---|
| GET | `/p03` | Strategic Radar interface |
| GET | `/p03/config` | Active thresholds/catalog/configuration |
| GET | `/p03/sources` | Approved source registry view |
| POST | `/p03/signals/assess` | Verify evidence, score and route signal |
| POST | `/p03/approve` | Record protected human decision |
| GET | `/health` | Service/config health |
| GET | `/docs` | OpenAPI explorer |

The complete synthetic request is at `../synthetic/verified-signal.json`. Production approval endpoints must bind roles to signed enterprise identity claims; request text is only a POC control.
