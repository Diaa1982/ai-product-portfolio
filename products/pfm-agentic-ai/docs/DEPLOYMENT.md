# Deployment

## Local candidate

```bash
cp products/pfm-agentic-ai/deploy/.env.example products/pfm-agentic-ai/deploy/.env
docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml up --build -d
curl http://localhost:8080/health
```

The command center is at `http://localhost:8080/p01`. Stop with `docker compose -f products/pfm-agentic-ai/deploy/docker-compose.yml down`.

## Production gate

Choose an approved hosting environment; pin base images and dependencies; add TLS, SSO/RBAC, secrets management, persistent evidence/audit storage, backups, monitoring, alert routing, WAF/network policy, vulnerability scanning and rollback. Configure only validated source-system interfaces. Complete legal/security/privacy/accounting/control review, UAT and a limited pilot before a go-live decision.
