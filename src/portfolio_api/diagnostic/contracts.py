from __future__ import annotations
from dataclasses import asdict,dataclass,field
from datetime import datetime,timezone
import uuid
def now():return datetime.now(timezone.utc).isoformat()
@dataclass
class Finding:
    finding_id:str;engagement_id:str;agent:str;domain:str;title:str;statement:str;evidence_ids:list[str]
    severity:str="medium";confidence:float=0.5;status:str="draft";limitations:list[str]=field(default_factory=list)
    recommendation:str="";human_review_required:bool=True;created_at:str=field(default_factory=now)
    def to_dict(self):return asdict(self)
    @classmethod
    def create(cls,engagement_id,agent,domain,title,statement,evidence_ids,**kw):
        return cls("FND-"+uuid.uuid4().hex[:10].upper(),engagement_id,agent,domain,title,statement,evidence_ids,**kw)
@dataclass
class ReviewDecision:
    finding_id:str;decision:str;reviewer_role:str;reason:str;decided_at:str=field(default_factory=now)
    def __post_init__(self):
        if self.decision not in {"approved","modified","rejected","returned"}:raise ValueError("Invalid decision")
