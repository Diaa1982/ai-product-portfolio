from __future__ import annotations
from typing import Any
class EnterpriseGRCReview:
    def review(self,rows:list[dict[str,Any]])->dict[str,Any]:
        findings=[]
        for r in rows:
            missing=[x for x in ("risk","control","owner") if not r.get(x)]
            if missing:findings.append({"code":"GRC_TRACEABILITY_GAP","severity":"high" if "control" in missing else "medium","statement":f"{r.get('risk_id') or r.get('evidence_id')}: missing {', '.join(missing)}","evidence_ids":[r["evidence_id"]],"recommendation":"Complete risk-control-owner traceability and validate operating evidence."})
        return {"record_count":len(rows),"traceability_complete":sum(1 for r in rows if r.get("risk") and r.get("control") and r.get("owner")),"findings":findings,"limitations":["Register completeness does not prove control operating effectiveness."]}
