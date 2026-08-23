# P15 deployment

Run `docker compose -f products/enterprise-architecture-intelligence/deploy/docker-compose.yml up --build` from the repository root. This synthetic profile is non-root, read-only and drops Linux capabilities. Production repository adapters, identity, security, migration, observability, resilience and approvals remain separate gates.
