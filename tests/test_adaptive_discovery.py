from src.portfolio_api.diagnostic.discovery import AdaptiveDiscovery

def test_adaptive_discovery_unknown_does_not_fabricate_confidence():
    d=AdaptiveDiscovery();matrix=d.matrix({},{"processes":[],"kpis":[],"grc":[]},[],["Processes"])
    qs=d.next_questions(matrix,[])
    assert qs and qs[0]["id"]=="PROC-OWN-01"
    a=d.answer(qs[0]["id"],"I don't know","unknown")
    matrix2=d.matrix({},{"processes":[],"kpis":[],"grc":[]},[a],["Processes"])
    row=next(x for x in matrix2 if x["question_id"]==qs[0]["id"])
    assert row["status"]=="unknown" and row["confidence"]==0

def test_structured_evidence_suppresses_redundant_questions():
    d=AdaptiveDiscovery();matrix=d.matrix({},{"processes":[{"process_id":"P1"}],"kpis":[],"grc":[]},[],["Processes"])
    assert all(x["status"]=="confirmed" for x in matrix)
    assert d.next_questions(matrix,[])==[]
    assert d.readiness(matrix,[])=="sufficient"
