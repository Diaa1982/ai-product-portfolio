import { eq, sql } from "drizzle-orm";
import { getDb } from "../../../../db";
import { projects } from "../../../../db/schema";

const stages = new Set(["Discover", "Evaluate", "Prioritize", "Approve", "Develop", "Deploy", "Operate", "Retire"]);
const risks = new Set(["Not assessed", "Low", "Moderate", "High", "Critical"]);

export async function PATCH(request: Request, context: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await context.params;
    const payload = (await request.json()) as Record<string, unknown>;
    const stage = typeof payload.stage === "string" && stages.has(payload.stage) ? payload.stage : undefined;
    const riskLevel = typeof payload.riskLevel === "string" && risks.has(payload.riskLevel) ? payload.riskLevel : undefined;
    const gateProgress = percent(payload.gateProgress);
    const values = { ...(stage ? { stage } : {}), ...(riskLevel ? { riskLevel } : {}), ...(gateProgress !== null ? { gateProgress } : {}), financialKpi: optionalPercent(payload.financialKpi), operationalKpi: optionalPercent(payload.operationalKpi), customerKpi: optionalPercent(payload.customerKpi), qualityKpi: optionalPercent(payload.qualityKpi), innovationKpi: optionalPercent(payload.innovationKpi), kpiPeriod: typeof payload.kpiPeriod === "string" ? payload.kpiPeriod.trim().slice(0, 30) || null : null, updatedAt: sql`CURRENT_TIMESTAMP` };
    const [project] = await getDb().update(projects).set(values).where(eq(projects.id, id)).returning();
    if (!project) return Response.json({ error: "Project not found" }, { status: 404 });
    return Response.json({ project });
  } catch (error) { return Response.json({ error: error instanceof Error ? error.message : "Unexpected error" }, { status: 500 }); }
}

function percent(value: unknown) { const number = typeof value === "number" ? value : Number(value); return Number.isFinite(number) ? Math.max(0, Math.min(100, number)) : null; }
function optionalPercent(value: unknown) { return value === null || value === "" || value === undefined ? null : percent(value); }
