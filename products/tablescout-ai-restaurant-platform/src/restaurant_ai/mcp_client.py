from __future__ import annotations

import asyncio
import json
import os
import sys


async def smoke_test() -> dict:
    """Launch the stdio server, discover tools, and validate search/fetch/recommend calls."""
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError as exc:
        raise RuntimeError("Install MCP dependencies: pip install -e '.[mcp]'") from exc

    env = os.environ.copy()
    env.setdefault("RESTAURANT_AI_DATA", "data/restaurants.json")
    env.setdefault("RESTAURANT_AI_AUDIT", "audit/events.jsonl")
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "restaurant_ai.mcp_server"],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            discovered = await session.list_tools()
            search = await session.call_tool("search", {"query": "romantic halal dinner", "top_k": 2})
            recommendation = await session.call_tool(
                "recommend", {"query": "vegan lunch", "dietary": ["vegan"], "top_k": 2}
            )
            approval = await session.call_tool(
                "upsert_restaurant", {"record": {}, "actor": "smoke-test", "confirm_write": False}
            )
            return {
                "tools": [tool.name for tool in discovered.tools],
                "search_ok": not search.isError,
                "recommend_ok": not recommendation.isError,
                "write_gate_ok": not approval.isError and "approval_required" in str(approval.content),
            }


def main():
    result = asyncio.run(smoke_test())
    print(json.dumps(result, indent=2))
    if not all(result[key] for key in ("search_ok", "recommend_ok", "write_gate_ok")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

