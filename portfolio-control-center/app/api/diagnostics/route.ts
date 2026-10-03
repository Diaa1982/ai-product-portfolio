import {NextRequest,NextResponse} from "next/server";
export async function POST(req:NextRequest){const base=process.env.DIAGNOSTIC_API_URL||"http://127.0.0.1:8000";const r=await fetch(base+"/diagnostics",{method:"POST",headers:{"content-type":"application/json"},body:await req.text(),cache:"no-store"});return new NextResponse(r.body,{status:r.status,headers:{"content-type":"application/json"}})}
