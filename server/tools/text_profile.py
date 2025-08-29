"""Text profile tool for generating text profiles from text or document IDs."""

import re

from config.logging_config import get_logger
from config.settings import config
from schemas import TextProfile
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = get_logger(__name__)

_WORD_RE = re.compile(r"[A-Za-z]+")
_analyzer = SentimentIntensityAnalyzer()


def _read_doc(doc_id: str) -> str | None:
    """Read a document from the corpus.

    Args:
        doc_id: A string containing the document ID

    Returns:
        str | None: The document text or None if not found
    """
    corpus_path = config.get_corpus_path()
    path = corpus_path / doc_id
    if path.is_file():
        try:
            with path.open(encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.warning("Failed to read document %s: %s", doc_id, e)
    return None


def _tokenize(text: str) -> list[str]:
    """Tokenize a given text into a list of words.

    Args:
        text: A string containing the text to tokenize

    Returns:
        list[str]: A list of tokens
    """
    return [w.lower() for w in _WORD_RE.findall(text)]


def _flesch_reading_ease(text: str) -> float:
    """Calculate the Flesch Reading Ease score for a given text.

    Args:
        text: A string containing the text to analyze

    Returns:
        float: The Flesch Reading Ease score
    """
    words = _tokenize(text)
    if not words:
        return 0.0
    sentences = max(1, len(re.split(r"[.!?]+", text)))
    syllables = 0
    for w in words:
        groups = re.findall(r"[aeiouy]+", w)
        syllables += max(1, len(groups))
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))


def _top_terms(text: str, n_top: int = 10) -> list[str]:
    """Generate the top terms for a given text.

    Args:
        text: A string containing the text to analyze
        n_top: The number of top terms to return

    Returns:
        list[str]: A list of the top terms
    """
    # With a single-document corpus, max_df must be >= min_df in doc-count terms.
    # Use max_df=1.0 to avoid "max_df < min_df" errors.
    try:
        vec = TfidfVectorizer(
            max_df=1.0,  # safe for single-doc
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
    """Generate a text profile for a given text or document ID.

    Args:
        text_or_doc_id: A string containing text or a document ID

    Returns:
        TextProfile: A TextProfile object containing the text profile data
    """
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
