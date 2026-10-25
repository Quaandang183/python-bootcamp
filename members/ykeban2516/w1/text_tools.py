"""Text analysis tools for tokenization and word frequency ranking."""

from collections import Counter


def word_count(text: str) -> dict[str, int]:
    """Count case-insensitive frequency of words after stripping punctuation.

    Args:
        text: Input text string to analyze.

    Returns:
        A dictionary mapping lowercase words to their occurrences.
    """
    cleaned = text.lower()
    for punctuation in ".,!?;:":
        cleaned = cleaned.replace(punctuation, " ")
    return dict(Counter(cleaned.split()))


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Retrieve top k most frequent words sorted by count and alphabetical order.

    Args:
        text: Input text string to analyze.
        k: Maximum number of word-frequency pairs to return.

    Returns:
        A list of tuples (word, count) sorted by descending frequency and ascending word.
    """
    counts = word_count(text)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:max(k, 0)]

