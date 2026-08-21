# Deployment Guide

```bash
docker compose -f products/signal-detection-agent/deploy/docker-compose.yml up --build -d
curl --fail http://localhost:8080/health
```

Open `/p04`. `P04_CONFIG_PATH` selects the versioned configuration.

Promote only a reviewed, signed immutable image after approved source onboarding, representative-corpus validation, security/performance/recovery tests and UAT. Rollback stops ingestion/publication, preserves evidence/audit, restores the prior image/config, runs health and a synthetic detection, reconciles queues and requires service-owner authorization before reopening.
