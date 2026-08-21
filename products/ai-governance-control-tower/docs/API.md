# API

| Method | Path | Purpose |
|---|---|---|
| GET | `/p14` | Governance dashboard |
| GET | `/p14/config` | Risk, gate and control configuration |
| POST | `/p14/risk/classify` | Classify profile and controls |
| POST | `/p14/gates/evaluate` | Evaluate gate evidence/readiness |
| POST | `/p14/gates/approve` | Record authorized human decision |
| POST | `/p14/monitor` | Evaluate monitoring event and safe action |
| GET | `/health` | Service/config health |

Synthetic requests are in `../synthetic/`. Production identity must be server-side; clients cannot self-assert approver roles.
