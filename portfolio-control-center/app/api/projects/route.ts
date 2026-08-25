import { env } from "cloudflare:workers";
import { getDb } from "../../../db";
import { projects } from "../../../db/schema";
import { categories } from "../../../lib/portfolio-seed";
import { listProjects } from "../../../lib/project-service";

type Bucket = { put(key: string, value: ArrayBuffer, options?: { httpMetadata?: { contentType?: string } }): Promise<unknown>; delete(key: string): Promise<void> };
const allowedTypes = new Set(["application/pdf", "application/json", "application/zip", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]);

export async function GET() {
  try { return Response.json({ projects: await listProjects(), portfolioTestCount: 247 }); }
  catch (error) {
    console.error("portfolio.projects.get_failed", error);
    return Response.json({ error: message(error) }, { status: 500 });
  }
}

export async function POST(request: Request) {
  let uploadedKey: string | null = null;
  try {
    const form = await request.formData();
    const name = clean(form.get("name"), 120), category = clean(form.get("category"), 120);
    const owner = clean(form.get("owner"), 100) || "Unassigned", stage = clean(form.get("stage"), 40) || "Discover";
    const notes = clean(form.get("notes"), 1000);
    if (!name) return Response.json({ error: "Project name is required" }, { status: 400 });
    if (!categories.includes(category as (typeof categories)[number])) return Response.json({ error: "Select a registered portfolio category" }, { status: 400 });
    const id = `USR-${crypto.randomUUID().slice(0, 8).toUpperCase()}`;
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "").slice(0, 80) || id.toLowerCase();
    const file = form.get("document");
    let documentName: string | null = null, documentType: string | null = null;
    if (file instanceof File && file.size > 0) {
      if (file.size > 10 * 1024 * 1024) return Response.json({ error: "Document must be 10 MB or smaller" }, { status: 400 });
      if (!allowedTypes.has(file.type)) return Response.json({ error: "Use PDF, JSON, ZIP, DOCX or XLSX" }, { status: 400 });
      const bucket = (env as unknown as { BUCKET?: Bucket }).BUCKET;
      if (!bucket) throw new Error("Document storage is unavailable");
      uploadedKey = `projects/${id}/${crypto.randomUUID()}-${safeFilename(file.name)}`;
      await bucket.put(uploadedKey, await file.arrayBuffer(), { httpMetadata: { contentType: file.type } });
      documentName = safeFilename(file.name); documentType = file.type;
    }
    const [project] = await getDb().insert(projects).values({ id, name, slug, category, owner, stage, notes, maturity: "uploaded-for-assessment", dataPolicy: "synthetic-only", productionReady: false, riskLevel: "Not assessed", gateProgress: 0, technicalStatus: "Pending validation", pilotWave: 4, documentKey: uploadedKey, documentName, documentType }).returning();
    return Response.json({ project }, { status: 201 });
  } catch (error) {
    if (uploadedKey) await (env as unknown as { BUCKET?: Bucket }).BUCKET?.delete(uploadedKey).catch(() => undefined);
    return Response.json({ error: message(error) }, { status: 500 });
  }
}

function clean(value: FormDataEntryValue | null, max: number) { return typeof value === "string" ? value.trim().slice(0, max) : ""; }
function safeFilename(value: string) { return value.replace(/[^a-zA-Z0-9._-]/g, "-").slice(0, 120); }
function message(error: unknown) { return error instanceof Error ? error.message : "Unexpected error"; }
