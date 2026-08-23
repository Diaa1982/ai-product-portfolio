# Deployment

Use `deploy/docker-compose.yml` for local synthetic deployment. CI builds P17 and smoke-tests health, UI, analysis and protected actions.

Production promotion requires segregated environments, signed artifacts, vulnerability gates, managed secrets, observability, backup/restore, RTO/RPO, capacity, rollback and change approval.
