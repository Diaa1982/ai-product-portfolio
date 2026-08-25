import assert from "node:assert/strict";
import { readFile, stat } from "node:fs/promises";
import test from "node:test";

test("build emits the governed portfolio deployment bundle", async () => {
  const hosting = JSON.parse(await readFile("dist/.openai/hosting.json", "utf8"));
  const clientManifest = await readFile("dist/client/.vite/manifest.json", "utf8");
  const serverBundle = await readFile("dist/server/index.js", "utf8");
  const migration = await readFile("dist/.openai/drizzle/0000_violet_magus.sql", "utf8");
  const socialCard = await stat("dist/client/og.jpg");

  assert.equal(hosting.project_id, "appgprj_6a8c8e0faa8c8191b52c848947f898ad");
  assert.equal(hosting.d1, "DB");
  assert.equal(hosting.r2, "BUCKET");
  assert.match(clientManifest, /portfolio-dashboard/);
  assert.match(serverBundle, /cloudflare:workers/);
  assert.match(migration, /CREATE TABLE `projects`/);
  assert.ok(socialCard.size > 40_000, "social preview image should be emitted");
});
