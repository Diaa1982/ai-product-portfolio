# Deployment Guide

```bash
docker compose -f products/strategic-radar/deploy/docker-compose.yml up --build -d
curl --fail http://localhost:8080/health
```

Open `/p03`. The active configuration is `config/radar.v1.json` and can be overridden by `P03_CONFIG_PATH`.

Production promotion requires a reviewed immutable commit/image, SBOM and vulnerability scan, signature, approved source configuration, test deployment, representative-corpus validation, security/performance/recovery tests, UAT, control approvals and the same image digest promoted to production. Roll back to the prior approved image/config; stop deliveries; preserve evidence/audit; verify health and a synthetic signal before reopening.
