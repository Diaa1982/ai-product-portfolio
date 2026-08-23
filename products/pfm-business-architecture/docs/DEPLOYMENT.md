# Deployment

Use `deploy/docker-compose.yml` for local synthetic deployment. CI builds the image and smoke-tests `/health` and `/p13/config`.

Production requires segregated environments, signed artifacts, vulnerability gates, approved infrastructure, managed secrets, logs/metrics/traces, backup/restore, tested RTO/RPO, capacity, rollback and change approval.
