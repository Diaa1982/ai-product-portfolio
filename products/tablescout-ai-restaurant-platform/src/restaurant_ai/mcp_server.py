from __future__ import annotations

import os

from .agents import RecommendationCrew
from .models import Restaurant, UserPreferences
from .retrieval import MultimodalRetriever
from .store import KnowledgeBase


def create_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install MCP dependencies: pip install -e '.[mcp]'") from exc

    server = FastMCP("restaurant-knowledge")
    data = os.getenv("RESTAURANT_AI_DATA", "data/restaurants.json")
    audit = os.getenv("RESTAURANT_AI_AUDIT", "audit/events.jsonl")

    @server.tool()
    def search(query: str, top_k: int = 5) -> dict:
        """Search active restaurants and return compact, citation-ready result metadata."""
        kb = KnowledgeBase(data, audit)
        hits = MultimodalRetriever(kb.load()).search(UserPreferences(query=query), top_k=min(max(top_k, 1), 10))
        return {"results": [{"id": h.restaurant.id, "title": h.restaurant.name,
                             "url": f"restaurant://{h.restaurant.id}", "score": round(h.fused_score, 4)} for h in hits]}

    @server.tool()
    def fetch(restaurant_id: str) -> dict:
        """Fetch a validated restaurant record by stable ID."""
        record = KnowledgeBase(data, audit).get(restaurant_id)
        if not record:
            raise ValueError("Restaurant not found")
        return {"id": record.id, "title": record.name, "text": record.model_dump_json(),
                "url": f"restaurant://{record.id}", "metadata": {"price_band": record.price_band.value}}

    @server.tool()
    def recommend(query: str, dietary: list[str] | None = None, max_price_band: str | None = None,
                  neighborhood: str | None = None, top_k: int = 3) -> dict:
        """Return ranked, evidence-grounded recommendations after applying hard filters."""
        payload = {"query": query, "dietary": dietary or [], "max_price_band": max_price_band,
                   "neighborhood": neighborhood}
        prefs = UserPreferences.model_validate(payload)
        kb = KnowledgeBase(data, audit)
        output, trace = RecommendationCrew(MultimodalRetriever(kb.load())).recommend(prefs, top_k=min(top_k, 5))
        return {"recommendations": [x.model_dump(mode="json") for x in output],
                "trace": [x.__dict__ for x in trace]}

    @server.tool()
    def upsert_restaurant(record: dict, actor: str, confirm_write: bool = False) -> dict:
        """Validate and update one record. A host must obtain explicit approval before confirm_write=true."""
        if not confirm_write:
            return {"status": "approval_required", "message": "Review the validated payload and confirm the write."}
        validated = Restaurant.model_validate(record)
        KnowledgeBase(data, audit).upsert(validated, actor=actor)
        return {"status": "updated", "restaurant_id": validated.id}

    return server


def main():
    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()

