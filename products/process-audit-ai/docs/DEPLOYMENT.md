# Deployment

Run `docker compose -f products/process-audit-ai/deploy/docker-compose.yml up --build`. The image runs non-root, read-only and without Linux capabilities. Configure `P06_CONFIG_PATH`, persistent audit storage, SSO, secrets, TLS, monitoring and backup per environment. Verify `/health`, `/p06/config` and a synthetic `/p06/audit` call. Promote signed image/config pairs through development, test, UAT and production with recorded approvals and rollback to the prior pair.
