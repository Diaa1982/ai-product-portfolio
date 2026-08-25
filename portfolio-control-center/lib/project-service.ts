import { asc } from "drizzle-orm";
import { getDb } from "../db";
import { projects } from "../db/schema";
import { seedProjects } from "./portfolio-seed";

export async function ensurePortfolioSeeded() {
  const db = getDb();
  const existing = await db.select({ id: projects.id }).from(projects).limit(1);
  if (existing.length === 0) await db.insert(projects).values(seedProjects).onConflictDoNothing();
}

export async function listProjects() {
  await ensurePortfolioSeeded();
  return getDb().select().from(projects).orderBy(asc(projects.pilotWave), asc(projects.id));
}
