from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    doc_id: str = Field(..., description="Document identifier (filename).")
    snippet: str = Field(..., description="Short text excerpt.")
    score: float = Field(..., description="Similarity score (0..1).")

class AnswerWithCitations(BaseModel):
    answer: str = Field(..., description="<=120-word synthesized answer.")
    sources: List[Source] = Field(..., description="1-5 supporting sources.")

class TextProfile(BaseModel):
    char_count: int
    token_count: int
    type_token_ratio: float
    top_ngrams: list[str]
    readability_flesch: float
    sentiment: float
    keywords: list[str]
