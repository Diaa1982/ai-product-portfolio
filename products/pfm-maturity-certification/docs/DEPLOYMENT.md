# Deployment

Use `deploy/docker-compose.yml` for a local synthetic deployment. CI builds the image and smoke-tests health, UI, evidenced maturity and certificate denial.

Production needs segregated environments, signed artifacts/configuration, vulnerability gates, managed secrets, observability, backup/restore, tested RTO/RPO, capacity, rollback and scheme-owner change approval.
