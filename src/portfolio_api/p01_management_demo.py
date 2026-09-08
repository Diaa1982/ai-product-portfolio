from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = REPO_ROOT / "products" / "pfm-agentic-ai" / "frontend"
CONFIG_PATH = Path(
    os.getenv(
        "P01_CONFIG_PATH",
        REPO_ROOT / "products" / "pfm-agentic-ai" / "config" / "pfm-agents.v1.json",
    )
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_text(url: str, timeout: int = 6) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PFM-Agentic-AI-Management-Demo/1.0 (+public-sector research demo)",
            "Accept": "application/json, application/rss+xml, application/xml, text/html;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_html(value: str) -> str:
    value = re.sub(r"<script[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


@dataclass
class Signal:
    signal_id: str
    title: str
    scope: str
    category: str
    source_name: str
    source_url: str
    source_type: str
    source_status: str
    published_at: str | None
    retrieved_at: str
    fact: str
    interpretation: str
    fiscal_exposure: list[str]
    horizon: str
    direction: str
    materiality: int
    confidence: int
    evidence_type: str = "LIVE_EXTERNAL"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SignalService:
    """Public-source signal adapter with explicit live/degraded provenance."""

    world_bank_series = {
        "NY.GDP.MKTP.KD.ZG": ("Real GDP growth", "Growth", ["Revenue", "Demand forecast"]),
        "FP.CPI.TOTL.ZG": ("Consumer price inflation", "Inflation", ["Expenditure", "Procurement", "Forecast"]),
    }

    def _world_bank(self) -> list[Signal]:
        out: list[Signal] = []
        for code, (label, category, exposure) in self.world_bank_series.items():
            url = f"https://api.worldbank.org/v2/country/ARE/indicator/{code}?format=json&mrnev=2"
            try:
                payload = json.loads(fetch_text(url))
                rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
                valid = [row for row in rows if row.get("value") is not None]
                if not valid:
                    continue
                latest = valid[0]
                prior = valid[1] if len(valid) > 1 else None
                latest_value = float(latest["value"])
                prior_value = float(prior["value"]) if prior and prior.get("value") is not None else None
                delta = latest_value - prior_value if prior_value is not None else None
                direction = "Higher" if delta is not None and delta > 0 else "Lower" if delta is not None and delta < 0 else "Stable"
                fact = f"{label} for UAE: {latest_value:.2f}% in {latest.get('date')}."
                if prior_value is not None:
                    fact += f" Previous available observation: {prior_value:.2f}%."
                interpretation = (
                    "This change may affect selected fiscal assumptions; it is an external statistical observation, not an approved budget assumption."
                )
                out.append(
                    Signal(
                        signal_id=f"wb-{code.lower()}", title=f"{label}: {direction}", scope="REGIONAL",
                        category=category, source_name="World Bank Indicators API", source_url=url,
                        source_type="OFFICIAL_API", source_status="LIVE", published_at=str(latest.get("date")),
                        retrieved_at=utc_now(), fact=fact, interpretation=interpretation,
                        fiscal_exposure=exposure, horizon="Medium term", direction=direction,
                        materiality=72 if category == "Growth" else 67, confidence=98,
                    )
                )
            except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, IndexError, KeyError):
                continue
        return out

    def _official_page_headlines(self, source_name: str, url: str, scope: str, limit: int = 3) -> list[Signal]:
        """Best-effort public page adapter. Failures are surfaced, never converted to fake live signals."""
        try:
            html = fetch_text(url)
        except (urllib.error.URLError, TimeoutError):
            return []
        candidates = re.findall(r"<(?:h1|h2|h3)[^>]*>(.*?)</(?:h1|h2|h3)>", html, flags=re.I | re.S)
        titles: list[str] = []
        for candidate in candidates:
            title = clean_html(candidate)
            if 20 <= len(title) <= 220 and title.lower() not in {x.lower() for x in titles}:
                titles.append(title)
            if len(titles) >= limit:
                break
        out: list[Signal] = []
        for idx, title in enumerate(titles):
            category = "Government Direction" if scope == "LOCAL" else "Macro Policy"
            out.append(
                Signal(
                    signal_id=f"page-{scope.lower()}-{idx}", title=title, scope=scope, category=category,
                    source_name=source_name, source_url=url, source_type="OFFICIAL_WEB",
                    source_status="LIVE", published_at=None, retrieved_at=utc_now(),
                    fact=f"New/current item published on the authoritative {source_name} public channel.",
                    interpretation="Requires fiscal analyst classification before it is used in a forecast, priority or budget recommendation.",
                    fiscal_exposure=["Strategy", "Fiscal assumptions"], horizon="To be assessed",
                    direction="Watch", materiality=55, confidence=90,
                )
            )
        return out

    def collect(self) -> dict[str, Any]:
        signals = self._world_bank()
        signals += self._official_page_headlines("International Monetary Fund", "https://www.imf.org/en/news", "GLOBAL", 2)
        signals += self._official_page_headlines("Government of Dubai Media Office", "https://mediaoffice.ae/en/", "LOCAL", 3)
        custom_sources = os.getenv("PFM_SIGNAL_SOURCES_JSON", "").strip()
        if custom_sources:
            try:
                for item in json.loads(custom_sources):
                    signals += self._official_page_headlines(
                        str(item["name"]), str(item["url"]), str(item.get("scope", "REGIONAL")).upper(), int(item.get("limit", 2))
                    )
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                pass
        return {
            "mode": "HYBRID_LIVE_EXTERNAL_SYNTHETIC_INTERNAL",
            "retrieved_at": utc_now(),
            "live_signal_count": len(signals),
            "signals": [s.to_dict() for s in signals],
            "provenance_rule": "Only successfully retrieved authoritative public evidence is labelled LIVE.",
        }


BASE_ENTITIES = [
    {"id": "A", "name": "Entity A · Health", "approved": 12.8, "adjusted": 12.9, "actual": 7.4, "commitments": 2.2, "accrual": 7.8, "cash_paid": 6.9, "forecast": 12.5, "monthly_request": 0.91, "modelled_need": 0.88, "delay_m": 0.08, "risk": "Low"},
    {"id": "B", "name": "Entity B · Education", "approved": 10.6, "adjusted": 10.8, "actual": 6.8, "commitments": 2.1, "accrual": 7.1, "cash_paid": 6.2, "forecast": 10.9, "monthly_request": 0.74, "modelled_need": 0.70, "delay_m": 0.16, "risk": "Medium"},
    {"id": "C", "name": "Entity C · Infrastructure", "approved": 8.4, "adjusted": 8.6, "actual": 4.1, "commitments": 3.2, "accrual": 4.8, "cash_paid": 3.7, "forecast": 9.2, "monthly_request": 0.78, "modelled_need": 0.51, "delay_m": 0.62, "risk": "High"},
    {"id": "D", "name": "Entity D · Public Safety", "approved": 6.9, "adjusted": 6.9, "actual": 4.5, "commitments": 1.2, "accrual": 4.6, "cash_paid": 4.2, "forecast": 6.8, "monthly_request": 0.49, "modelled_need": 0.48, "delay_m": 0.05, "risk": "Low"},
    {"id": "E", "name": "Entity E · Government Services", "approved": 3.8, "adjusted": 3.9, "actual": 2.1, "commitments": 0.7, "accrual": 2.2, "cash_paid": 1.8, "forecast": 3.5, "monthly_request": 0.31, "modelled_need": 0.29, "delay_m": 0.03, "risk": "Low"},
]

BASE_REVENUE = {"approved": 48.6, "actual_ytd": 32.9, "forecast": 47.8, "cash_collected": 32.2, "receivables": 2.4}
BASE_TREASURY = {"cash_balance": 9.2, "seven_day": 9.2, "thirty_day": 7.8, "sixty_day": 6.1, "ninety_day": 5.4, "surplus_investable": 2.1}


class ScenarioRequest(BaseModel):
    scenario: str = Field(pattern=r"^(baseline|revenue_shock|capital_delay|cash_pressure|close_exception)$")


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class ReportRequest(BaseModel):
    report_type: str = "Budget Execution"
    entity_id: str | None = None
    mandate: str = "All mandates"
    period: str = "Year to date"
    include_forecast: bool = True
    include_delays: bool = True
    include_exceptions: bool = True
    include_evidence: bool = True


class DemoState:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> dict[str, Any]:
        self.scenario = "baseline"
        self.entities = deepcopy(BASE_ENTITIES)
        self.revenue = deepcopy(BASE_REVENUE)
        self.treasury = deepcopy(BASE_TREASURY)
        self.events: list[dict[str, Any]] = []
        self.run_id = f"DEMO-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        self._record("Control Plane", "Demo environment reset", "Synthetic PFM baseline restored", "completed")
        return self.snapshot()

    def _record(self, agent: str, action: str, detail: str, status: str = "running") -> None:
        self.events.insert(0, {"agent": agent, "action": action, "detail": detail, "status": status, "time": utc_now()})
        self.events = self.events[:100]

    def apply(self, name: str) -> dict[str, Any]:
        self.reset()
        self.scenario = name
        if name == "revenue_shock":
            self.revenue["forecast"] = 45.1
            self.revenue["actual_ytd"] = 31.8
            self.treasury["ninety_day"] = 4.7
            self._record("Signal Intelligence", "External downside signal accepted for simulation", "Live evidence remains separate from the synthetic impact scenario")
            self._record("Revenue Forecast", "Downside revenue scenario calculated", "Synthetic forecast reduced by AED 2.7B")
            self._record("Fiscal Strategy", "Fiscal envelope review prepared", "Management options generated; no budget authority exercised", "waiting_approval")
        elif name == "capital_delay":
            c = next(e for e in self.entities if e["id"] == "C")
            c["forecast"] = 9.35
            c["delay_m"] = 0.78
            c["risk"] = "High"
            self._record("Entity Monitor", "Material capital delay detected", "Entity C delay exposure increased to AED 780M", "exception")
            self._record("Budget Execution", "Forecast outturn recalculated", "Entity C forecast now exceeds adjusted budget", "exception")
        elif name == "cash_pressure":
            c = next(e for e in self.entities if e["id"] == "C")
            c["monthly_request"] = 0.92
            c["modelled_need"] = 0.51
            self.treasury["thirty_day"] = 6.9
            self._record("Cash Forecast", "Funding request challenged", "AED 920M requested vs AED 510M modelled need", "exception")
            self._record("Authority Gate", "Funding instruction blocked", "Treasury approval required before any release", "waiting_approval")
        elif name == "close_exception":
            self._record("Accounting Operations", "Month-end close exception", "3 bank reconciliations and 12 inter-entity confirmations remain open", "exception")
            self._record("Government Consolidation", "Consolidation readiness reduced", "Draft statements remain non-certifiable", "waiting_approval")
        else:
            self._record("Fiscal Health", "Baseline fiscal pulse completed", "No scenario shock applied")
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        approved = round(sum(e["approved"] for e in self.entities), 2)
        adjusted = round(sum(e["adjusted"] for e in self.entities), 2)
        actual = round(sum(e["actual"] for e in self.entities), 2)
        commitments = round(sum(e["commitments"] for e in self.entities), 2)
        accrual = round(sum(e["accrual"] for e in self.entities), 2)
        cash_paid = round(sum(e["cash_paid"] for e in self.entities), 2)
        forecast = round(sum(e["forecast"] for e in self.entities), 2)
        high_risk = sum(1 for e in self.entities if e["risk"] == "High")
        forecast_variance = round((forecast - adjusted) / adjusted * 100, 2) if adjusted else 0
        health = max(0, min(100, round(90 - high_risk * 7 - max(0, forecast_variance) * 1.2 - max(0, 5.0 - self.treasury["ninety_day"]) * 2)))
        return {
            "run_id": self.run_id,
            "scenario": self.scenario,
            "data_classification": "SIMULATED_INTERNAL",
            "entities": deepcopy(self.entities),
            "revenue": deepcopy(self.revenue),
            "treasury": deepcopy(self.treasury),
            "totals": {
                "approved": approved, "adjusted": adjusted, "actual": actual,
                "commitments": commitments, "accrual": accrual, "cash_paid": cash_paid,
                "forecast": forecast, "forecast_variance_percent": forecast_variance,
                "fiscal_health_index": health,
            },
            "events": deepcopy(self.events),
            "generated_at": utc_now(),
        }

    def ask(self, question: str) -> dict[str, Any]:
        q = question.lower()
        worst = max(self.entities, key=lambda e: ((e["forecast"] - e["adjusted"]), e["delay_m"]))
        if any(term in q for term in ["exceed", "over budget", "overspend"]):
            answer = f"{worst['name']} has the strongest synthetic overrun signal: forecast AED {worst['forecast']:.2f}B versus adjusted budget AED {worst['adjusted']:.2f}B."
            evidence = ["synthetic entity budget ledger", "forecast outturn"]
        elif "delay" in q and "cash" in q:
            matches = [e for e in self.entities if e["delay_m"] >= 0.15 and e["monthly_request"] > e["modelled_need"]]
            names = ", ".join(e["name"] for e in matches) or "No entity"
            answer = f"{names} meets the current synthetic condition of material delay plus a funding request above modelled monthly need."
            evidence = ["synthetic delay register", "synthetic cash forecast"]
        elif "revenue" in q or "outlook" in q:
            answer = f"Synthetic revenue forecast is AED {self.revenue['forecast']:.1f}B versus approved revenue AED {self.revenue['approved']:.1f}B. Current scenario: {self.scenario}."
            evidence = ["synthetic revenue plan", "scenario engine"]
        elif "cash" in q or "liquidity" in q:
            answer = f"The synthetic 30-day cash position is AED {self.treasury['thirty_day']:.1f}B and the 90-day position is AED {self.treasury['ninety_day']:.1f}B."
            evidence = ["synthetic treasury forecast"]
        elif "accrual" in q or "account" in q:
            totals = self.snapshot()["totals"]
            answer = f"Synthetic accrued expense is AED {totals['accrual']:.1f}B while cash paid is AED {totals['cash_paid']:.1f}B, a difference of AED {totals['accrual'] - totals['cash_paid']:.1f}B requiring timing and liability analysis."
            evidence = ["synthetic accrual ledger", "synthetic cash ledger"]
        else:
            answer = f"Fiscal Health Index is {self.snapshot()['totals']['fiscal_health_index']}/100 in the current synthetic scenario. The highest-risk entity is {worst['name']}."
            evidence = ["synthetic fiscal health model"]
        return {
            "answer": answer,
            "recommendation": "Use the identified evidence to prepare a management review; protected financial actions remain subject to authorized human approval.",
            "evidence": evidence,
            "confidence": 95,
            "classification": "AI_INFERENCE_OVER_SYNTHETIC_INTERNAL_DATA",
            "question": question,
        }

    def report(self, req: ReportRequest) -> dict[str, Any]:
        rows = self.entities
        if req.entity_id:
            rows = [e for e in rows if e["id"] == req.entity_id]
            if not rows:
                raise ValueError("Unknown entity_id")
        exceptions = []
        for e in rows:
            if e["forecast"] > e["adjusted"]:
                exceptions.append(f"{e['name']}: forecast exceeds adjusted budget by AED {e['forecast'] - e['adjusted']:.2f}B")
            if e["delay_m"] >= 0.15:
                exceptions.append(f"{e['name']}: delayed expenditure exposure AED {e['delay_m']:.2f}B")
            if e["monthly_request"] > e["modelled_need"] * 1.15:
                exceptions.append(f"{e['name']}: monthly funding request materially exceeds modelled need")
        return {
            "title": req.report_type,
            "mandate": req.mandate,
            "period": req.period,
            "status": "EVIDENCE_LINKED_DRAFT",
            "data_classification": "SIMULATED_INTERNAL",
            "rows": deepcopy(rows),
            "totals": self.snapshot()["totals"],
            "exceptions": exceptions if req.include_exceptions else [],
            "forecast_included": req.include_forecast,
            "delays_included": req.include_delays,
            "evidence": ["synthetic budget ledger", "synthetic commitments", "synthetic cash/accrual bridge"] if req.include_evidence else [],
            "generated_at": utc_now(),
            "authority_note": "This is a management-demo draft, not an approved statutory report or financial statement.",
        }


signal_service = SignalService()
state = DemoState()

app = FastAPI(
    title="PFM Agentic AI — Management Demo",
    version="1.0.0-demo",
    description="Hybrid live-external/synthetic-internal management demonstration for governed agentic public finance management.",
)
app.mount("/assets", StaticFiles(directory=FRONTEND), name="assets")


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "product": "P01", "mode": "management-demo", "time": utc_now()}


@app.get("/", include_in_schema=False)
def root() -> FileResponse:
    return FileResponse(FRONTEND / "management-demo.html")


@app.get("/command-center", include_in_schema=False)
def command_center() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/config")
def config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


@app.get("/api/signals")
def signals() -> dict[str, Any]:
    return signal_service.collect()


@app.get("/api/fiscal")
def fiscal() -> dict[str, Any]:
    return state.snapshot()


@app.get("/api/agents")
def agents() -> dict[str, Any]:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    latest = state.events
    result = []
    for agent in cfg.get("agents", []):
        matching = [e for e in latest if agent["name"].split(" Agent")[0].lower() in e["agent"].lower()]
        result.append({
            **agent,
            "runtime_status": matching[0]["status"] if matching else "idle",
            "last_activity": matching[0] if matching else None,
            "data_classification": "CONFIGURATION_AND_SYNTHETIC_RUNTIME",
        })
    return {"agents": result, "events": latest, "generated_at": utc_now()}


@app.post("/api/scenario")
def scenario(req: ScenarioRequest) -> dict[str, Any]:
    return state.apply(req.scenario)


@app.post("/api/reset")
def reset() -> dict[str, Any]:
    return state.reset()


@app.post("/api/ask")
def ask(req: AskRequest) -> dict[str, Any]:
    return state.ask(req.question)


@app.post("/api/reports")
def reports(req: ReportRequest) -> dict[str, Any]:
    try:
        return state.report(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
