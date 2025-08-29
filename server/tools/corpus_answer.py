"""Corpus answer tool for answering queries using the corpus."""

import re

from config.logging_config import get_logger
from config.settings import config
from schemas import AnswerWithCitations, Source
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = get_logger(__name__)

_vectorizer = None
_matrix = None
_doc_ids: list[str] = []
_docs: list[str] = []

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _load_corpus() -> tuple[list[str], list[str]]:
    """Load the corpus from the corpus directory.

    Returns:
        tuple[list[str], list[str]]: A tuple containing the document IDs and texts
    """
    corpus_path = config.get_corpus_path()
    paths = sorted(corpus_path.glob("*.txt"))
    ids, texts = [], []
    for p in paths:
        try:
            with p.open(encoding="utf-8") as f:
                txt = f.read()
            did = p.name
            ids.append(did)
            texts.append(txt)
        except Exception as e:
            logger.warning("Failed to load corpus file %s: %s", p, e)
    return ids, texts


def _ensure_index() -> None:
    """Ensure the TF-IDF index is built.

    This function ensures that the TF-IDF index is built and stored in memory.
    It also ensures that the document IDs and texts are loaded from the corpus.
    """
    global _vectorizer, _matrix, _doc_ids, _docs
    if _vectorizer is not None:
        return
    _doc_ids, _docs = _load_corpus()
    if not _docs:
        _doc_ids = ["README.txt"]
        _docs = ["Add .txt files to server/data/corpus to enable corpus answering."]

    _vectorizer = TfidfVectorizer(
        max_df=config.tfidf_max_df,
        min_df=config.tfidf_min_df,
        ngram_range=config.tfidf_ngram_range,
        stop_words="english",
    )
    _matrix = _vectorizer.fit_transform(_docs)
    logger.info("Built TF-IDF index with %d documents", len(_docs))


def _synthesize_answer(text: str, limit_words: int | None = None) -> str:
    """Synthesize an answer from a given text.

    Args:
        text: A string containing the text to synthesize
        limit_words: An integer containing the maximum number of words to include in the answer

    Returns:
        str: A string containing the synthesized answer
    """
    if limit_words is None:
        limit_words = config.max_answer_words

    sents = _SENT_SPLIT.split(text.strip())
    snippet = " ".join(sents[:2]).strip()
    words = snippet.split()
    if len(words) > limit_words:
        snippet = " ".join(words[:limit_words]) + "…"
    return snippet or (text[:400] + "…")


def corpus_answer(query: str) -> AnswerWithCitations:
    """Answer a query using the corpus.

    Args:
        query: A string containing the query to answer

    Returns:
        AnswerWithCitations: An AnswerWithCitations object containing the answer and sources
    """
    _ensure_index()
    qv = _vectorizer.transform([query])
    sims = cosine_similarity(qv, _matrix).ravel()
    top_idx = sims.argsort()[::-1][: config.top_sources_count]

    sources: list[Source] = []
    for i in top_idx:
        score = float(max(0.0, min(1.0, sims[i])))
        snippet = _synthesize_answer(_docs[i], limit_words=config.max_snippet_words)
        sources.append(Source(doc_id=_doc_ids[i], snippet=snippet, score=score))

    answer_text = _synthesize_answer(
        _docs[top_idx[0]], limit_words=config.max_answer_words
    )
    return AnswerWithCitations(
        answer=answer_text, sources=sources[: config.top_sources_count]
    )
