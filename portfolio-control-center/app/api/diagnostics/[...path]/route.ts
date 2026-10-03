import {NextRequest,NextResponse} from "next/server";
const base=()=>process.env.DIAGNOSTIC_API_URL||"http://127.0.0.1:8000";
async function forward(req:NextRequest,parts:string[]){
 const path=parts.join("/"); const url=base()+"/diagnostics/"+path+req.nextUrl.search;
 const headers=new Headers(req.headers);headers.delete("host");
 const init:RequestInit={method:req.method,headers,cache:"no-store"};
 if(!["GET","HEAD"].includes(req.method))init.body=await req.arrayBuffer();
 const r=await fetch(url,init);return new NextResponse(r.body,{status:r.status,headers:{"content-type":r.headers.get("content-type")||"application/json","content-disposition":r.headers.get("content-disposition")||""}});
}
export async function GET(req:NextRequest,{params}:{params:Promise<{path:string[]}>}){return forward(req,(await params).path)}
export async function POST(req:NextRequest,{params}:{params:Promise<{path:string[]}>}){return forward(req,(await params).path)}
