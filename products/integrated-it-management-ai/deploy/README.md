# P16 container

From the repository root, run `docker compose -f products/integrated-it-management-ai/deploy/docker-compose.yml up --build`. Open `/p16`; health is `/health`. The image runs as a non-root user with a read-only filesystem and a dedicated runtime volume. Production secrets, TLS, IAM, approved adapters, observability and recovery controls remain deployment responsibilities.
