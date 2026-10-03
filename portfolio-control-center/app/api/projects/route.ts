// Staging compatibility route. The portfolio project registry remains Cloudflare/D1-backed.
export async function GET(){return Response.json({projects:[],portfolioTestCount:247,notice:"Project registry is disabled in diagnostic staging."})}
export async function POST(){return Response.json({error:"Project registry writes are disabled in diagnostic staging."},{status:503})}
