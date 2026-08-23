# Deployment

Use `deploy/docker-compose.yml` for local synthetic deployment. CI builds the image and smoke-tests health, UI, traceability/impact and protected actions.

Production requires segregated environments, signed artifacts/config, vulnerability gates, managed secrets, observability, backup/restore, RTO/RPO, capacity, rollback and controlled repository adapters.
