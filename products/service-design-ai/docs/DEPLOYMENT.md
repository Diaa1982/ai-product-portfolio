# Deployment

Build with `docker compose -f products/service-design-ai/deploy/docker-compose.yml up --build`. The non-root, read-only container drops Linux capabilities and exposes port 8080. Configure `P05_CONFIG_PATH`, persistent audit storage, approved SSO, secrets, TLS, observability and backups per environment. Verify `/health`, `/p05/config` and a synthetic `/p05/design` call. Promote signed images through development, test, UAT and production with recorded approvals; roll back to the prior signed image/config pair.
