import os
from dotenv import load_dotenv
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from fastmcp import FastMCP
from schemas import AnswerWithCitations, TextProfile
from tools.corpus_answer import corpus_answer
from tools.text_profile import text_profile

# Load environment variables
load_dotenv()

# Quickstart-style server instance
mcp = FastMCP(name="scholarlens", instructions="Academic retrieval + text analytics demo")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@mcp.tool
def corpus_answer_tool(query: str) -> AnswerWithCitations:
    """Answer a question from the local corpus with short citations."""
    return corpus_answer(query)

@mcp.tool
def text_profile_tool(text_or_doc_id: str) -> TextProfile:
    """Compute basic text analytics for a doc_id or raw text."""
    return text_profile(text_or_doc_id)

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8765"))
    # Run via HTTP transport so the dockerized client can connect using a URL
    mcp.run(transport="http", host=host, port=port)
