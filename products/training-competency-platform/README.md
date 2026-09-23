# Training, Assessment & Competency Management System

**Status:** A runnable local FastAPI/PostgreSQL MVP package exists, and this branch also contains an earlier browser-only HTML demonstration. Neither is a public hosted application or a production-ready enterprise service. The earlier `index.html` in this GitHub directory is NOT the connected MVP frontend.

## Project documentation
- [File inventory and version distinction](docs/FILE_MANIFEST.md)
- [Docker Compose and local execution](docs/LOCAL_DEPLOYMENT.md)
- [Functional requirements and workflow](docs/PRODUCT_REQUIREMENTS.md)
- [Implemented database and enterprise target](docs/DATABASE.md)
- [API endpoints and contracts](docs/API.md)
- [System architecture and build roadmap](docs/ARCHITECTURE.md)
- [Frontend and UX design options](docs/FRONTEND_UX.md)
- [Security, audit and pilot limitations](docs/SECURITY_AND_ASSURANCE.md)

## What the executable MVP does
Using synthetic material, authorized demonstration roles can upload and approve knowledge, create a programme and modules, author and approve multiple-choice questions, publish programmes, enroll a learner, complete sequential assessments, calculate overall and critical-control scores, block or unlock progression and review basic result and audit records. Six demo identities are selected through an insecure request header, not real authentication. AI generation, vector retrieval, full version-controlled enterprise schema, narrative grading and production audit protection are planned, not implemented.

## Run locally
From the deployable ZIP's extracted project directory, copy `.env.example` to `.env`, set `POSTGRES_PASSWORD`, then run `docker compose up --build -d`. Open `http://localhost:8000` for the **connected frontend** and `http://localhost:8000/docs` for API documentation. Default `APP_BIND=127.0.0.1` intentionally restricts access to the host computer. The source files `app/main.py` and `web/index.html` are part of the deployable ZIP, distinct from this branch's early standalone HTML.

## Project principle
Approved evidence before AI outputs; deterministic scoring; examiner approval before publication; role-specific experiences; repeatable attempt history. Never use confidential documents or actual employee data in this unsecured demonstration.
