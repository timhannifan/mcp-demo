"""Main application for the MCP server."""

from config.logging_config import setup_logging
from config.settings import config
from fastmcp import FastMCP
from schemas import AnswerWithCitations, TextProfile
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from tools.corpus_answer import corpus_answer
from tools.text_profile import text_profile

# Setup logging with config
setup_logging(level=config.log_level, format_string=config.log_format)

# Quickstart-style server instance
mcp = FastMCP(name=config.app_name, instructions=config.app_instructions)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    """Health check endpoint."""
    if not config.health_check_enabled:
        return PlainTextResponse("Health check disabled", status_code=503)
    return PlainTextResponse("OK")


@mcp.custom_route("/reload", methods=["POST"])
async def reload_corpus(request: Request) -> PlainTextResponse:
    """Reload the corpus from disk."""
    try:
        # Clear the existing index
        import tools.corpus_answer
        from tools.corpus_answer import _ensure_index

        tools.corpus_answer._vectorizer = None
        tools.corpus_answer._matrix = None
        tools.corpus_answer._doc_ids = []
        tools.corpus_answer._docs = []

        # Rebuild the index
        _ensure_index()
        return PlainTextResponse("Corpus reloaded successfully")
    except Exception as e:
        return PlainTextResponse(f"Error reloading corpus: {e}", status_code=500)


@mcp.tool
def corpus_answer_tool(query: str) -> AnswerWithCitations:
    """Answer a question from the local corpus with short citations."""
    return corpus_answer(query)


@mcp.tool
def text_profile_tool(text_or_doc_id: str) -> TextProfile:
    """Compute basic text analytics for a doc_id or raw text."""
    return text_profile(text_or_doc_id)


if __name__ == "__main__":
    mcp_config = config.get_mcp_config()
    # Run via HTTP transport so the dockerized client can connect using a URL
    mcp.run(transport="http", host=mcp_config["host"], port=mcp_config["port"])
