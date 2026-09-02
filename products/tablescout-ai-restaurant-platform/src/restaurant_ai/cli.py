from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .ingestion import extract_restaurant
from .models import Dietary, PriceBand, UserPreferences
from .sample_data import records
from .store import KnowledgeBase


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="restaurant-ai", description="Restaurant knowledge-base control plane")
    parser.add_argument("--data", default=os.getenv("RESTAURANT_AI_DATA", "data/restaurants.json"))
    parser.add_argument("--audit", default=os.getenv("RESTAURANT_AI_AUDIT", "audit/events.jsonl"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed", help="Create validated demo data")
    sub.add_parser("validate", help="Validate schema and uniqueness")
    sub.add_parser("list", help="List restaurant summaries")
    show = sub.add_parser("show", help="Show one restaurant")
    show.add_argument("restaurant_id")
    upsert = sub.add_parser("upsert", help="Validate and safely upsert one JSON record")
    upsert.add_argument("json_file")
    upsert.add_argument("--actor", required=True)
    recommend = sub.add_parser("recommend", help="Run the recommendation crew")
    recommend.add_argument("query")
    recommend.add_argument("--dietary", action="append", default=[])
    recommend.add_argument("--cuisine", action="append", default=[])
    recommend.add_argument("--neighborhood")
    recommend.add_argument("--max-price", choices=[x.value for x in PriceBand])
    recommend.add_argument("--top-k", type=int, default=3)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    kb = KnowledgeBase(args.data, args.audit)
    if args.command == "seed":
        kb.replace_all(records(), actor="cli:seed")
        print(f"Seeded {len(records())} restaurants into {args.data}")
    elif args.command == "validate":
        ok, errors = kb.validate()
        print(json.dumps({"valid": ok, "errors": errors}, indent=2))
        return 0 if ok else 1
    elif args.command == "list":
        print(json.dumps([{"id": r.id, "name": r.name, "rating": r.average_rating} for r in kb.load()], indent=2))
    elif args.command == "show":
        record = kb.get(args.restaurant_id)
        print(record.model_dump_json(indent=2) if record else "Not found")
        return 0 if record else 1
    elif args.command == "upsert":
        payload = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        kb.upsert(extract_restaurant(payload), actor=args.actor)
        print("Upsert completed and audited")
    elif args.command == "recommend":
        from .agents import RecommendationCrew
        from .retrieval import MultimodalRetriever
        prefs = UserPreferences(query=args.query, cuisines=args.cuisine,
            dietary=[Dietary(x) for x in args.dietary],
            max_price_band=PriceBand(args.max_price) if args.max_price else None,
            neighborhood=args.neighborhood)
        recommendations, traces = RecommendationCrew(MultimodalRetriever(kb.load())).recommend(prefs, top_k=args.top_k)
        print(json.dumps({"recommendations": [x.model_dump() for x in recommendations],
                          "trace": [x.__dict__ for x in traces]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

