from __future__ import annotations
from html import escape
from io import BytesIO
def render_html(report):
    e=report["engagement"];rows="".join(f"<article><h3>{escape(x['title'])}</h3><p><b>{escape(x['domain'])}</b> · {escape(x['severity'])}</p><p>{escape(x['statement'])}</p><p><b>Evidence:</b> {escape(', '.join(x.get('evidence_ids',[])))}</p><p><b>Recommendation:</b> {escape(x.get('recommendation',''))}</p></article>" for x in report["approved_findings"])
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Diagnostic Report</title><style>body{{font:15px Arial;max-width:900px;margin:40px auto;color:#14212b}}h1{{font-size:32px}}article{{border-top:1px solid #ccd5da;padding:18px 0}}.notice{{background:#eef7f4;padding:16px}}</style></head><body><p>TRANSFORMATION INTELLIGENCE · CONTROLLED DIAGNOSTIC</p><h1>{escape(e.get('organization','Diagnostic'))}</h1><p>{escape(e.get('objective',''))}</p><h2>Executive synthesis</h2><p>{escape((report.get('executive_synthesis') or {}).get('statement',''))}</p><h2>Human-approved findings</h2>{rows or '<p>No findings have been approved for publication.</p>'}<p class='notice'>{escape(report['notice'])}</p></body></html>"""
def render_pdf(report):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
    except ImportError as e:raise RuntimeError("PDF rendering requires reportlab") from e
    b=BytesIO();doc=SimpleDocTemplate(b,pagesize=A4);s=getSampleStyleSheet();story=[Paragraph("Transformation Intelligence — Controlled Diagnostic",s["Title"]),Paragraph(report["engagement"].get("organization",""),s["Heading2"]),Paragraph(report["engagement"].get("objective",""),s["BodyText"]),Spacer(1,12),Paragraph("Executive synthesis",s["Heading2"]),Paragraph((report.get("executive_synthesis") or {}).get("statement",""),s["BodyText"])]
    for f in report["approved_findings"]:story += [Spacer(1,10),Paragraph(f["title"],s["Heading3"]),Paragraph(f["statement"],s["BodyText"]),Paragraph("Evidence: "+", ".join(f.get("evidence_ids",[])),s["BodyText"]),Paragraph("Recommendation: "+f.get("recommendation",""),s["BodyText"])]
    story += [Spacer(1,16),Paragraph(report["notice"],s["Italic"])];doc.build(story);return b.getvalue()
