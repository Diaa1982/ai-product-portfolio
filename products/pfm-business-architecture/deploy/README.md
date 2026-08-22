# P13 deployment

From the repository root, run `docker compose -f products/pfm-business-architecture/deploy/docker-compose.yml up --build`. This profile is synthetic-only and hardened with a non-root user, read-only filesystem, dropped capabilities and a health check. Production secrets, IAM, residency, integrations, observability and recovery remain deployment-approval gates.
