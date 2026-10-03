from __future__ import annotations
import os
from pathlib import Path
from fastapi import APIRouter,File,Form,HTTPException,UploadFile
from pydantic import BaseModel
from .diagnostic import DiagnosticRuntime

router=APIRouter(prefix="/diagnostics",tags=["diagnostics"])
runtime=DiagnosticRuntime(Path(os.getenv("DIAGNOSTIC_STORE_PATH","data/runtime/diagnostics")))

class DiagnosticCreate(BaseModel):
    id:str;organization:str;objective:str="";priorities:list[str]=[]
class ExecuteRequest(BaseModel):
    domains:list[str]
class DecisionRequest(BaseModel):
    decision:str;reviewer_role:str;reason:str;modified_statement:str|None=None

@router.post("")
def create_diagnostic(body:DiagnosticCreate):
    try:return runtime.create(body.model_dump())
    except Exception as e:raise HTTPException(400,str(e))

@router.post("/{engagement_id}/evidence")
async def upload_evidence(engagement_id:str,file:UploadFile=File(...),classification:str=Form("Internal")):
    data=await file.read()
    if len(data)>25*1024*1024:raise HTTPException(413,"Evidence file exceeds 25 MB staging limit")
    try:return runtime.upload(engagement_id,file.filename or "evidence",file.content_type or "application/octet-stream",data,classification).to_dict()
    except (ValueError,RuntimeError) as e:raise HTTPException(400,str(e))

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
def report(engagement_id:str):
    try:return runtime.report(engagement_id)
    except KeyError:raise HTTPException(404,"Diagnostic engagement not found")
