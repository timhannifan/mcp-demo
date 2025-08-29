"""Schemas for the MCP server."""

from pydantic import BaseModel, Field


class Source(BaseModel):
    """Source model."""

    doc_id: str = Field(..., description="Document identifier (filename).")
    snippet: str = Field(..., description="Short text excerpt.")
    score: float = Field(..., description="Similarity score (0..1).")


class AnswerWithCitations(BaseModel):
    """Answer with citations model."""

    answer: str = Field(..., description="<=120-word synthesized answer.")
    sources: list[Source] = Field(..., description="1-5 supporting sources.")


class TextProfile(BaseModel):
    """Text profile model."""

    char_count: int
    token_count: int
    type_token_ratio: float
    top_ngrams: list[str]
    readability_flesch: float
    sentiment: float
    keywords: list[str]
