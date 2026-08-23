# API

| Method | Path | Purpose |
|---|---|---|
| GET | `/p09` | KPI review interface |
| GET | `/p09/config` | Schema/status configuration |
| POST | `/p09/review` | Validate, calculate and prepare review |
| POST | `/p09/approve` | Record owner/executive decision |
| GET | `/health` | Service/config health |

The synthetic request is in `../synthetic/kpi-review.json`. Production upload endpoints must use controlled file/object ingestion and authenticated approver roles.
