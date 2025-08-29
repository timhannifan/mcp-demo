"""Smoke test for the MCP server."""

import asyncio
import os
from pprint import pprint

from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()


async def main() -> None:
    """Main function to test the MCP server."""
    url = os.environ.get("MCP_SERVER_URL", "http://localhost:8765/mcp")
    client = Client(url)

    async with client:
        await client.ping()
        print("✅ Server is reachable")

        tools = await client.list_tools()
        print("\nAvailable tools:")
        pprint(tools)

        print("\nCalling corpus_answer_tool …")
        r1 = await client.call_tool(
            "corpus_answer_tool",
            {"query": "How do urban transport policies affect emissions and health?"},
        )
        pprint(r1.data)

        print("\nCalling text_profile_tool …")
        r2 = await client.call_tool(
            "text_profile_tool", {"text_or_doc_id": "air_quality_health.txt"}
        )
        pprint(r2.data)


if __name__ == "__main__":
    asyncio.run(main())
