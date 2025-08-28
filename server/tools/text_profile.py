import os, re
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from schemas import TextProfile

_CORPUS_DIR = os.getenv("CORPUS_DIR", "data/corpus")
_WORD_RE = re.compile(r"[A-Za-z]+")

_analyzer = SentimentIntensityAnalyzer()

def _read_doc(doc_id: str) -> str | None:
    path = os.path.join(_CORPUS_DIR, doc_id)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def _tokenize(text: str) -> List[str]:
    return [w.lower() for w in _WORD_RE.findall(text)]

def _flesch_reading_ease(text: str) -> float:
    words = _tokenize(text)
    if not words: return 0.0
    sentences = max(1, len(re.split(r"[.!?]+", text)))
    syllables = 0
    for w in words:
        groups = re.findall(r"[aeiouy]+", w)
        syllables += max(1, len(groups))
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))

def _top_terms(text: str, n_top: int = 10) -> list[str]:
    # With a single-document corpus, max_df must be >= min_df in doc-count terms.
    # Use max_df=1.0 to avoid "max_df < min_df" errors.
    try:
        vec = TfidfVectorizer(
            max_df=1.0,           # safe for single-doc
            min_df=1,
            ngram_range=(1, 2),
            stop_words="english",
        )
        X = vec.fit_transform([text])
        if X.shape[1] == 0:
            return []
        scores = X.toarray()[0]
        feats = vec.get_feature_names_out()
        order = scores.argsort()[::-1][:n_top]
        return [feats[i] for i in order]
    except Exception:
        # Fallback: simple frequency top unigrams/bigrams (no IDF)
        tokens = _tokenize(text)
        if not tokens:
            return []
        from collections import Counter
        unigrams = [" ".join([t]) for t in tokens]
        bigrams = [" ".join(pair) for pair in zip(tokens, tokens[1:])]
        counts = Counter(unigrams + bigrams)
        return [w for w, _ in counts.most_common(n_top)]


def text_profile(text_or_doc_id: str) -> TextProfile:
    text = _read_doc(text_or_doc_id) or text_or_doc_id
    chars = len(text)
    tokens = _tokenize(text)
    token_count = len(tokens)
    ttr = (len(set(tokens)) / token_count) if token_count else 0.0
    readability = _flesch_reading_ease(text)
    sentiment = _analyzer.polarity_scores(text)["compound"]
    ngrams = _top_terms(text, n_top=10)
    keywords = ngrams[:10]
    return TextProfile(
        char_count=chars,
        token_count=token_count,
        type_token_ratio=round(ttr, 4),
        top_ngrams=ngrams,
        readability_flesch=round(readability, 2),
        sentiment=round(sentiment, 4),
        keywords=keywords,
    )
