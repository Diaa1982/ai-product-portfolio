# API Summary

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Platform status and control flags |
| GET | `/products` | Product register |
| GET | `/workflows` | Configured product workflows |
| GET | `/cases` | Case register, optionally filtered by product |
| POST | `/cases` | Create a validated case |
| GET | `/cases/{case_id}` | Retrieve full case record |
| POST | `/cases/{case_id}/evidence` | Attach classified evidence |
| POST | `/cases/{case_id}/evaluate` | Run calculations and controlled evaluation |
| POST | `/cases/{case_id}/submit` | Submit to the configured human gate |
| POST | `/cases/{case_id}/decision` | Approve, reject or return using the required role |
| GET | `/cases/{case_id}/audit/verify` | Verify the audit hash chain |

## Evidence minimum fields

```json
{
  "evidence_id": "EV-SYN-001",
  "source_id": "SYNTHETIC-BUDGET",
  "source_version": "1.0",
  "content_hash": "sha256-value",
  "classification": "SYNTHETIC"
}
```

## Error behavior

- `400` invalid state, missing inputs/evidence or invalid decision.
- `403` role lacks the configured approval authority.
- `404` case does not exist.
- `422` request structure fails API validation.
