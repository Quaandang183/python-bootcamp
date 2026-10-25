"""W1-2: word counting helpers."""

_PUNCT = str.maketrans("", "", ".,!?;:")


def word_count(text: str) -> dict[str, int]:
    """Count words, ignoring case and basic punctuation."""
    counts: dict[str, int] = {}
    for w in text.lower().translate(_PUNCT).split():
        counts[w] = counts.get(w, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the ``k`` most frequent words, ties broken alphabetically."""
    items = sorted(word_count(text).items(), key=lambda kv: (-kv[1], kv[0]))
    return items[:k]
