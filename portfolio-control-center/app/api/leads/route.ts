export async function POST(request:Request){
 const body=await request.json().catch(()=>null);
 if(!body||typeof body.name!=="string"||typeof body.email!=="string"||typeof body.organization!=="string"||body.consent!=="yes") return Response.json({ok:false,error:"invalid_request"},{status:400});
 const email=/^[^\s@]+@[^\s@]+\.[^\s@]+$/; if(!email.test(body.email)||body.name.length>120||body.email.length>160||body.organization.length>160) return Response.json({ok:false,error:"invalid_fields"},{status:400});
 const lead={id:crypto.randomUUID(),createdAt:new Date().toISOString(),name:body.name.trim(),email:body.email.trim().toLowerCase(),organization:body.organization.trim(),role:String(body.role||"").slice(0,120),country:String(body.country||"").slice(0,100),interest:String(body.interest||"").slice(0,160),message:String(body.message||"").slice(0,2000),source:String(body.source||"website").slice(0,100)};
 const webhook=process.env.LEAD_WEBHOOK_URL;
 if(webhook){const result=await fetch(webhook,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(lead)});if(!result.ok)return Response.json({ok:false,error:"handoff_failed"},{status:502})}
 else console.log("LEAD_CAPTURE",JSON.stringify(lead));
 return Response.json({ok:true,id:lead.id});
}