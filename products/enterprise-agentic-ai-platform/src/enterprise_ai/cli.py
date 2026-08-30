from __future__ import annotations

import argparse
import json

from .config import get_settings
from .schemas import UseCaseRequest
from .workflow_crewai import run_crewai
from .workflow_langgraph import EnterpriseLangGraphWorkflow


def parser() -> argparse.ArgumentParser:
    item = argparse.ArgumentParser(description="Enterprise Agentic AI starter kit")
    item.add_argument("challenge", help="Enterprise problem or opportunity")
    item.add_argument("--title", default="Enterprise AI Use Case")
    item.add_argument("--objective", default="")
    item.add_argument("--profile", default="ai_transformation")
    item.add_argument("--orchestrator", choices=["langgraph", "crewai"], default="langgraph")
    return item


def main() -> None:
    args = parser().parse_args()
    request = UseCaseRequest(
        title=args.title,
        challenge=args.challenge,
        objective=args.objective,
        use_case_type=args.profile,
    )
    settings = get_settings()
    if args.orchestrator == "crewai":
        print(run_crewai(request, settings))
    else:
        result = EnterpriseLangGraphWorkflow(settings).run(request)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()

