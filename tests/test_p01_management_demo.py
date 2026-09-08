from src.portfolio_api.p01_management_demo import DemoState, ReportRequest


def test_baseline_is_coherent():
    state = DemoState()
    snap = state.snapshot()
    assert snap["data_classification"] == "SIMULATED_INTERNAL"
    assert snap["totals"]["approved"] > 0
    assert round(sum(e["actual"] for e in snap["entities"]), 2) == snap["totals"]["actual"]
    assert all(e["actual"] <= e["accrual"] for e in snap["entities"])


def test_revenue_shock_changes_forecast_not_approved_plan():
    state = DemoState()
    before = state.snapshot()
    after = state.apply("revenue_shock")
    assert after["revenue"]["approved"] == before["revenue"]["approved"]
    assert after["revenue"]["forecast"] < before["revenue"]["forecast"]
    assert any(e["status"] == "waiting_approval" for e in after["events"])


def test_cash_pressure_creates_authority_gate():
    state = DemoState()
    snap = state.apply("cash_pressure")
    c = next(e for e in snap["entities"] if e["id"] == "C")
    assert c["monthly_request"] > c["modelled_need"]
    assert any(e["agent"] == "Authority Gate" and e["status"] == "waiting_approval" for e in snap["events"])


def test_report_filters_entity_and_disclaims_authority():
    state = DemoState()
    report = state.report(ReportRequest(entity_id="C", report_type="Entity Fiscal Position"))
    assert len(report["rows"]) == 1
    assert report["rows"][0]["id"] == "C"
    assert "not an approved statutory report" in report["authority_note"]


def test_ask_pfm_uses_synthetic_evidence():
    state = DemoState()
    result = state.ask("Which entities may exceed budget?")
    assert "Entity C" in result["answer"]
    assert result["classification"] == "AI_INFERENCE_OVER_SYNTHETIC_INTERNAL_DATA"
    assert result["evidence"]


def test_reset_restores_baseline():
    state = DemoState()
    state.apply("capital_delay")
    reset = state.reset()
    c = next(e for e in reset["entities"] if e["id"] == "C")
    assert reset["scenario"] == "baseline"
    assert c["delay_m"] == 0.62
