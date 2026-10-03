from __future__ import annotations
import os
from pathlib import Path
from fastapi import APIRouter,File,Form,HTTPException,UploadFile
from fastapi.responses import HTMLResponse,Response
from .diagnostic.reporting import render_html,render_pdf
from pydantic import BaseModel
from .diagnostic import DiagnosticRuntime

router=APIRouter(prefix="/diagnostics",tags=["diagnostics"])
runtime=DiagnosticRuntime(Path(os.getenv("DIAGNOSTIC_STORE_PATH","data/runtime/diagnostics")))

class DiagnosticCreate(BaseModel):
    id:str;organization:str;objective:str="";priorities:list[str]=[]
class ExecuteRequest(BaseModel):
    domains:list[str]
class DiscoveryAnswerRequest(BaseModel):
    question_id:str;answer:str;precision:str="qualitative";note:str|None=None
class DecisionRequest(BaseModel):
    decision:str;reviewer_role:str;reason:str;modified_statement:str|None=None

@router.post("")
def create_diagnostic(body:DiagnosticCreate):
    try:return runtime.create(body.model_dump())
    except Exception as e:raise HTTPException(400,str(e))

@router.get("/{engagement_id}")
def get_diagnostic(engagement_id:str):
    try:return runtime.get(engagement_id)
    except KeyError:raise HTTPException(404,"Diagnostic engagement not found")

@router.post("/{engagement_id}/evidence")
async def upload_evidence(engagement_id:str,file:UploadFile=File(...),classification:str=Form("Internal")):
    data=await file.read()
    if len(data)>25*1024*1024:raise HTTPException(413,"Evidence file exceeds 25 MB staging limit")
    try:return runtime.upload(engagement_id,file.filename or "evidence",file.content_type or "application/octet-stream",data,classification).to_dict()
    except (ValueError,RuntimeError) as e:raise HTTPException(400,str(e))

@router.post("/{engagement_id}/discover")
def discover(engagement_id:str,body:ExecuteRequest):
    try:return runtime.discover(engagement_id,body.domains)
    except KeyError:raise HTTPException(404,"Diagnostic engagement not found")

@router.post("/{engagement_id}/discovery/answer")
def answer_discovery(engagement_id:str,body:DiscoveryAnswerRequest):
    try:return runtime.answer_discovery(engagement_id,body.question_id,body.answer,body.precision,body.note)
    except KeyError:raise HTTPException(404,"Diagnostic engagement or question not found")
    except ValueError as e:raise HTTPException(400,str(e))

@router.post("/{engagement_id}/execute")
def execute(engagement_id:str,body:ExecuteRequest):
    try:return runtime.execute(engagement_id,body.domains)
    except KeyError:raise HTTPException(404,"Diagnostic engagement not found")

@router.post("/{engagement_id}/findings/{finding_id}/decision")
def decide(engagement_id:str,finding_id:str,body:DecisionRequest):
    try:return runtime.decide(engagement_id,finding_id,body.decision,body.reviewer_role,body.reason,body.modified_statement)
    except KeyError:raise HTTPException(404,"Diagnostic or finding not found")
    except ValueError as e:raise HTTPException(400,str(e))

@router.get("/{engagement_id}/report")
def report(engagement_id:str,format:str="json"):
    try:
        data=runtime.report(engagement_id)
        if format=="html":return HTMLResponse(render_html(data))
        if format=="pdf":return Response(render_pdf(data),media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="{engagement_id}-diagnostic.pdf"'})
        return data
    except KeyError:raise HTTPException(404,"Diagnostic engagement not found")
    except RuntimeError as e:raise HTTPException(500,str(e))
