# GitHub Pilot Validation Workflow

The **Pilot Validation** workflow provides a controlled, repeatable way to test any of the 18 product candidates from GitHub. It validates code and controls, builds the selected Docker image, runs a synthetic-only container, verifies health and the product dashboard, and uploads a dated evidence package.

It is a validation workflow, not a hosting or production-deployment workflow.

## Start a run

After this workflow is merged into `main`:

1. Open **Actions** in the repository.
2. Select **Pilot Validation**.
3. Select **Run workflow**.
4. Choose a product. Begin with P08, then P14, then P16.
5. Choose the evidence stage: demonstration, staging-readiness or UAT-readiness.
6. Enter the approved pilot/change/review reference.
7. Keep the full portfolio test suite enabled for formal evidence.
8. Run the workflow and wait for a green result.
9. Download the `pilot-evidence-...` artifact from the run page.

## Controls enforced

- Only registered P01–P18 products can be selected.
- The registry must state `synthetic-only` and `production_ready=false`.
- The portfolio registry, tests, compilation and secret-file control are validated.
- The selected image is built from its registered product package.
- The container runs non-root as defined by the product Dockerfile, with a read-only filesystem, temporary runtime storage, dropped Linux capabilities and no-new-privileges.
- LLM access is disabled.
- Health and the selected product dashboard must respond successfully.
- The artifact records product, stage, reference, commit, actor, run URL, time and control outcomes.
- No environment deployment, production data onboarding or autonomous approval occurs.

## Pilot sequence

| Wave | Products | Governance purpose |
|---|---|---|
| 1 | P08 | Use-case intake, value, feasibility and prioritization |
| 2 | P14 | AI risk classification, control gates and human approval |
| 3 | P16 | Integrated IT service, change, portfolio, asset and risk oversight |
| 4 | Remaining products | Product-specific pilots after the applicable owners and controls approve scope |

PFM products must retain approved fiscal source definitions, delegations and segregation of duties. PEFA references remain diagnostic alignment metadata, and IPSAS-oriented outputs remain subject to authorized accounting review; the workflow never issues a formal assessment, compliance conclusion or financial authorization.

## Evidence and next gate

A successful run supports technical verification and pilot evidence. Before staging or UAT, complete the applicable L0–L10 requirements in the product go-live checklist, including owner approval, approved data scope, IAM, security/privacy, integration controls, UAT, operating ownership, continuity, residual-risk acceptance and formal release authority.

For a publicly accessible or internal staging URL, add a separate provider-specific deployment workflow only after the target hosting platform, environment, identity model and secrets approach are approved.
