from __future__ import annotations
import csv, io, json, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

class EvidenceExtractor:
    MAX_TEXT=500_000
    def extract(self,filename:str,media_type:str,data:bytes)->dict:
        ext=Path(filename).suffix.lower()
        if ext in {".txt",".md",".csv",".json"}:
            text=data.decode("utf-8",errors="replace")
            if ext==".csv":
                rows=list(csv.reader(io.StringIO(text)));text="\n".join(" | ".join(r) for r in rows)
        elif ext in {".docx",".pptx",".xlsx"}:
            text=self._openxml(data,ext)
        elif ext==".pdf":
            text=self._pdf(data)
        else: raise ValueError(f"Unsupported evidence type: {ext}")
        text=re.sub(r"\n{3,}","\n\n",text).strip()[:self.MAX_TEXT]
        return {"text":text,"characters":len(text),"status":"extracted" if text else "empty","extractor":"diagnostic-v1"}
    def _openxml(self,data,ext):
        names={".docx":("word/",".xml"),".pptx":("ppt/slides/",".xml"),".xlsx":("xl/",".xml")}
        prefix,suffix=names[ext];parts=[]
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for n in sorted(z.namelist()):
                if n.startswith(prefix) and n.endswith(suffix):
                    try:
                        root=ET.fromstring(z.read(n));parts.extend(t.text for t in root.iter() if t.text and t.text.strip())
                    except ET.ParseError: pass
        return "\n".join(parts)
    def _pdf(self,data):
        try:
            from pypdf import PdfReader
        except ImportError as e: raise RuntimeError("PDF extraction requires pypdf") from e
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
