export async function GET(){return Response.json({error:"Project registry is disabled in diagnostic staging."},{status:503})}
export async function PATCH(){return Response.json({error:"Project registry writes are disabled in diagnostic staging."},{status:503})}
export async function DELETE(){return Response.json({error:"Project registry writes are disabled in diagnostic staging."},{status:503})}
