# P02 Container Package

Run from repository root:

```bash
docker compose -f products/pfm-brain/deploy/docker-compose.yml up --build
```

The container runs as a non-root user with dropped capabilities, a read-only filesystem and tmpfs demo runtime. Production still requires approved hosting, identity, persistent evidence/audit stores, integrations, monitoring, resilience and security assurance.
