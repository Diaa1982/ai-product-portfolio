# Deployment

```bash
cp products/revenue-reconciliation-ai/deploy/.env.example products/revenue-reconciliation-ai/deploy/.env
docker compose -f products/revenue-reconciliation-ai/deploy/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

Open `http://localhost:8080/p12`. This is a dummy-data technical candidate.

Before production: approve environment and network; sign/scan images; implement SSO/RBAC/SoD, secrets, persistent evidence/exception/audit stores, owner-approved source/bank/treasury/revenue/accounting adapters, monitoring, backup/DR and rollback; complete finance/tax/legal/security/privacy/control assurance, UAT and pilot.
