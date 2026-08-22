# Deployment

Run `docker compose -f products/partnership-management-copilot/deploy/docker-compose.yml up --build`. The reference image runs non-root, read-only and without Linux capabilities. Configure `P07_CONFIG_PATH`, persistent review/audit storage, TLS, monitoring and backup. Verify `/health`, `/p07/config` and the synthetic analysis. Production Microsoft 365 Copilot/SharePoint configuration is deployed separately through approved tenant governance; do not add background automation to this MVP.
