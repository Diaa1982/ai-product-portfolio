# Architecture

`Service Inventory → Assessment Case → Evidence Register → Method Workspace → AI Analysis → Human Validation → Gate Approval → Controlled Reports → Benefits Monitoring`

FastAPI exposes the P05 studio and JSON API. `ServiceDesignAI` loads the immutable versioned methodology configuration, validates inputs, applies deterministic classification and gate rules, structures journeys/blueprints/method prompts, and returns a SHA-256 audit digest. Production adapters for identity, document/evidence management, service catalogue, workflow, ALMAS cost inputs and monitoring are explicitly future integrations requiring approval.

AI-generated narrative never changes registers or gate state without an attributable human transaction. Configuration, model/prompt version, inputs, outputs, evidence and decisions must be retained together.
