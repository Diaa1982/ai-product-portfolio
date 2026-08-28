from __future__ import annotations

import asyncio
from pathlib import Path

from fastmcp.client import Client, PythonStdioTransport


async def discover_and_call(query: str) -> dict:
    server = Path(__file__).with_name("mcp_server.py")
    transport = PythonStdioTransport(script_path=str(server))
    async with Client(transport) as client:
        tools = await client.list_tools()
        result = await client.call_tool(
            "search_enterprise_knowledge", {"query": query, "k": 5}
        )
        return {
            "discovered_tools": [tool.name for tool in tools],
            "result": [getattr(item, "text", str(item)) for item in result.content],
        }


if __name__ == "__main__":
    print(asyncio.run(discover_and_call("enterprise AI governance")))

