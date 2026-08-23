# P17 deployment

From the repository root, run `docker compose -f products/pfm-cycle-time-benchmark/deploy/docker-compose.yml up --build`. This profile is synthetic-only and uses a non-root user, read-only filesystem, dropped capabilities and a health check. Production sources, licenses, operational data, IAM, integrations, observability, resilience and approvals remain separate gates.
