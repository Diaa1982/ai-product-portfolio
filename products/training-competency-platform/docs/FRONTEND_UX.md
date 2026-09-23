# Frontend design and user experience options

**Current connected UI:** `web/index.html` is a minimal, functional single-page frontend served by FastAPI. It has Overview, Knowledge, Design, Learner, Results and Audit sections. It uses the demo role selector and calls `/api`. The other package-root `index.html` is a browser-only prototype and is not the deployed UI.

## A. Enterprise operations console
Persistent navigation, task/KPI cards, searchable tables, filters, bulk actions, contextual drawers and approval queues. Suits knowledge owners, training managers, examiners and auditors managing many records. Risk: too dense for occasional learners.

## B. Guided training and assessment studio
Step-by-step wizard with clear progress and validations: upload → verify reference → objectives → blueprint → questions → examiner review → publication. Suits occasional examiners and training managers. Risk: extra steps for frequent users.

## C. Role-based hybrid
Manager/examiner/knowledge owner use a console plus guided high-risk workflows; learners use a separate distraction-free course and exam experience; auditors get read-only evidence and chronology. AI drafts and approved decisions have visibly different status. This is the proposed design direction for review, not a design decision already approved.

## Screen map
Global shell: organization/product, breadcrumb, EN/AR language switch, notifications and identity. Dashboard: my tasks and approval queue. Knowledge: upload, source list, preview, versions and approval. Programmes: catalogue, detail and builder. Assessment: blueprint, question bank, source/rubric panel and review. Learner: my learning, course, module, exam, results and remediation. Analytics: objective/cohort outcomes and qualified impact. Audit: events, decision evidence and controlled export.

## Critical user journeys
Examiner: dashboard → programme → assessment blueprint → author/generate draft → check citation/rubric → approve → publication readiness. Learner: assigned course → prerequisites → lesson → exam instructions → answer → review → submit → score/critical result → objective gaps → remediation/retry or next module. Knowledge owner: upload → extraction preview → metadata → approval. Auditor: decision chronology → source and scoring evidence.

## UX acceptance
Responsive 360/768/1200 px; mobile-first exam; accessible labels and visible keyboard focus; WCAG 2.2 AA target; inline validation; loading/empty/error/success states; clear locked-module reasons, remaining attempts and critical thresholds; confirmation for publication/submission; no fabricated autosave when backend lacks it; EN LTR and Arabic RTL designed together. Use reusable design tokens and components, not scattered hard-coded styles.

## Visual directions to choose independently
1. Institutional minimal: teal/slate/white.
2. Warm modern enterprise: teal/beige/soft brown.
3. Analytics-led: dark sidebar, high-contrast light content.

Choose A/B/C for interaction model and 1/2/3 for visual language. Also decide Arabic-first versus English-first and whether the first sprint must support mobile learners.