import { env } from "cloudflare:workers";
import { asc } from "drizzle-orm";
import { getDb } from "../db";
import { projects } from "../db/schema";
import { seedProjects } from "./portfolio-seed";

const insertSeedSql = `INSERT INTO projects (
  id, name, slug, category, owner, stage, maturity, data_policy,
  production_ready, risk_level, gate_progress, technical_status,
  pilot_wave, source_url, notes
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO NOTHING`;

export async function ensurePortfolioSeeded() {
  const db = getDb();
  const existing = await db.select({ id: projects.id }).from(projects).limit(1);
  if (existing.length === 0) {
    await env.DB.batch(seedProjects.map((project) => env.DB.prepare(insertSeedSql).bind(
      project.id,
      project.name,
      project.slug,
      project.category,
      project.owner,
      project.stage,
      project.maturity,
      project.dataPolicy,
      project.productionReady ? 1 : 0,
      project.riskLevel,
      project.gateProgress,
      project.technicalStatus,
      project.pilotWave,
      project.sourceUrl,
      project.notes,
    )));
  }
}

export async function listProjects() {
  await ensurePortfolioSeeded();
  return getDb().select().from(projects).orderBy(asc(projects.pilotWave), asc(projects.id));
}
