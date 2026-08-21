# Deployment Guide

```bash
docker compose -f products/corporate-performance-review-ai/deploy/docker-compose.yml up --build -d
curl --fail http://localhost:8080/health
```

Open `/p09`. `P09_CONFIG_PATH` selects the versioned KPI configuration.

Production promotion follows dev → test → production with peer review, product/business approval and security/legal review when controls change. Run schema, regression, security, performance, smoke, UAT and recovery tests. Rollback freezes publication, preserves files/evidence/audit, restores the prior image/config, validates a synthetic KPI review and requires service-owner reopening.
