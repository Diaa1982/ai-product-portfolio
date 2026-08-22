# Deployment
Run `docker compose -f products/enterprise-process-intelligence/deploy/docker-compose.yml up --build`. Verify `/health`, `/p10/config` and the synthetic analysis. Promote signed image/config pairs through development, test, UAT and production. Repository connectors, persistent graph/audit stores, SSO, monitoring, backup and rollback require approved production configuration.
