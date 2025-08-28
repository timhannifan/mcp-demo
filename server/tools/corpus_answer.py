import os, re, glob
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from schemas import AnswerWithCitations, Source

_CORPUS_DIR = os.getenv("CORPUS_DIR", "data/corpus")

_vectorizer = None
_matrix = None
_doc_ids: List[str] = []
_docs: List[str] = []

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def _load_corpus() -> Tuple[List[str], List[str]]:
    paths = sorted(glob.glob(os.path.join(_CORPUS_DIR, "*.txt")))
    ids, texts = [], []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                txt = f.read()
            did = os.path.basename(p)
            ids.append(did)
            texts.append(txt)
        except Exception:
            pass
    return ids, texts

def _ensure_index():
    global _vectorizer, _matrix, _doc_ids, _docs
    if _vectorizer is not None:
        return
    _doc_ids, _docs = _load_corpus()
    if not _docs:
        _doc_ids = ["README.txt"]
        _docs = ["Add .txt files to server/data/corpus to enable corpus answering."]
    _vectorizer = TfidfVectorizer(max_df=0.9, min_df=1, ngram_range=(1,2), stop_words="english")
    _matrix = _vectorizer.fit_transform(_docs)

def _synthesize_answer(text: str, limit_words: int = 120) -> str:
    sents = _SENT_SPLIT.split(text.strip())
    snippet = " ".join(sents[:2]).strip()
    words = snippet.split()
    if len(words) > limit_words:
        snippet = " ".join(words[:limit_words]) + "…"
    return snippet or (text[:400] + "…")

def corpus_answer(query: str) -> AnswerWithCitations:
    _ensure_index()
    qv = _vectorizer.transform([query])
    sims = cosine_similarity(qv, _matrix).ravel()
    top_idx = sims.argsort()[::-1][:5]
    sources: List[Source] = []
    for i in top_idx:
        score = float(max(0.0, min(1.0, sims[i])))
        snippet = _synthesize_answer(_docs[i], limit_words=60)
        sources.append(Source(doc_id=_doc_ids[i], snippet=snippet, score=score))
    answer_text = _synthesize_answer(_docs[top_idx[0]], limit_words=120)
    return AnswerWithCitations(answer=answer_text, sources=sources[:5])
