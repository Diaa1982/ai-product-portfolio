from __future__ import annotations
import hashlib, json, os, uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

def now(): return datetime.now(timezone.utc).isoformat()

@dataclass
class StoredEvidence:
    evidence_id:str; engagement_id:str; filename:str; media_type:str; size:int; content_hash:str
    object_key:str; classification:str; stored_at:str; extracted_text_path:str|None=None
    extraction_status:str="pending"; approved_for_use:bool=False
    def to_dict(self): return asdict(self)

class ObjectStore(Protocol):
    def put(self,key:str,data:bytes)->str: ...
    def get(self,key:str)->bytes: ...

class FileObjectStore:
    def __init__(self,root:str|Path): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def put(self,key,data):
        p=self.root/key;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);return str(p)
    def get(self,key): return (self.root/key).read_bytes()

class EvidenceRepository:
    def __init__(self,root:str|Path):
        self.root=Path(root);self.objects=FileObjectStore(self.root/"objects");self.index=self.root/"evidence.json"
    def _read(self):
        return json.loads(self.index.read_text()) if self.index.exists() else {}
    def _write(self,d):
        self.index.parent.mkdir(parents=True,exist_ok=True);tmp=self.index.with_suffix(".tmp");tmp.write_text(json.dumps(d,indent=2)+"\n");tmp.replace(self.index)
    def store(self,engagement_id,filename,media_type,data,classification="Internal"):
        eid="EVD-"+uuid.uuid4().hex[:10].upper();digest=hashlib.sha256(data).hexdigest();key=f"{engagement_id}/{eid}/{Path(filename).name}"
        self.objects.put(key,data);r=StoredEvidence(eid,engagement_id,Path(filename).name,media_type,len(data),digest,key,classification,now())
        d=self._read();d[eid]=r.to_dict();self._write(d);return r
    def update(self,eid,**fields):
        d=self._read();d[eid].update(fields);self._write(d);return StoredEvidence(**d[eid])
    def get(self,eid): return StoredEvidence(**self._read()[eid])
    def list(self,engagement_id): return [StoredEvidence(**x) for x in self._read().values() if x["engagement_id"]==engagement_id]
