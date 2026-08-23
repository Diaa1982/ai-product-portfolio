# Deployment Guide

```bash
docker compose -f products/ai-governance-control-tower/deploy/docker-compose.yml up --build -d
curl --fail http://localhost:8080/health
```

Open `/p14`. `P14_CONFIG_PATH` selects the versioned governance configuration.

Production promotion requires approved policies/roles/control catalog, enterprise identity and registers, reviewed signed image, security/non-functional testing, UAT, recovery exercise, residual-risk decisions and CEO G4 authorization. Rollback freezes gate decisions, preserves evidence/audit, restores the last approved image/config, validates health/risk/gate/monitoring scenarios and requires service-owner reopening authorization.
