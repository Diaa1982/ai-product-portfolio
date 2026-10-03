from __future__ import annotations
import csv,io,json,re
from typing import Any

def _lines(text): return [x.strip() for x in text.splitlines() if x.strip()]

class EvidenceNormalizer:
    """Conservative normalizer: emits engine-ready records only when required fields are explicit."""
    def normalize(self, texts:dict[str,str])->dict[str,Any]:
        return {"processes":self._processes(texts),"kpis":self._kpis(texts),"grc":self._grc(texts)}
    def _processes(self,texts):
        out=[]
        for eid,text in texts.items():
            for line in _lines(text):
                # PIPE schema: PROCESS|id|guid|name|level|owner|status|version|parent|notation
                p=[x.strip() for x in line.split("|")]
                if len(p)>=9 and p[0].upper()=="PROCESS":
                    out.append({"evidence_id":eid,"process_id":p[1],"process_guid":p[2],"name":p[3],"level":p[4],"owner_role":p[5],"status":p[6],"version":p[7],"parent_id":p[8] or None,"notation":p[9] if len(p)>9 else "APQC"})
        return out
    def _kpis(self,texts):
        out=[]
        for eid,text in texts.items():
            for line in _lines(text):
                # KPI|id|name|direction|frequency|aggregation|target|actual|period|evidence_ref
                p=[x.strip() for x in line.split("|")]
                if len(p)>=9 and p[0].upper()=="KPI":
                    try: target=float(p[6]);actual=float(p[7])
                    except ValueError: continue
                    out.append({"evidence_id":eid,"master":{"KPI_ID":p[1],"KPI_Name":p[2],"Direction":p[3],"Frequency":p[4],"Aggregation_Method":p[5],"Data_Source":eid},"result":{"Target":target,"Actual":actual,"Period":p[8],"Data_Status":"Official" if len(p)>9 and p[9] else "Draft","Evidence_Reference":p[9] if len(p)>9 else eid}})
        return out
    def _grc(self,texts):
        out=[]
        pat=re.compile(r"^(RISK|CONTROL|POLICY)\|([^|]+)\|(.+)$",re.I)
        for eid,text in texts.items():
            for line in _lines(text):
                m=pat.match(line)
                if m:out.append({"evidence_id":eid,"type":m.group(1).upper(),"id":m.group(2).strip(),"statement":m.group(3).strip()})
        return out
