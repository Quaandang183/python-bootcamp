"""Text analysis and frequency count utilities."""

import re
from collections import Counter


def word_count(text: str) -> dict[str, int]:
    """Count case-insensitive word frequencies in a given string.

    Punctuation is stripped and words are lowercased.

    Args:
        text: Input string to analyze.

    Returns:
        A dictionary mapping lowercase words to their occurrence count.
    """
    clean_txt = re.sub(r"[^\w\s]", "", text.lower())
    words = clean_txt.split()
    return dict(Counter(words))


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Find the top-k most frequent words in a string.

    Ties are sorted alphabetically.

    Args:
        text: Input string to analyze.
        k: Maximum number of top words to return.

    Returns:
        A list of (word, count) tuples of length at most k.
    """
    if not text:
        return []
    counts = word_count(text)
    word_sort = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return word_sort[:k]


top_K = top_k

if __name__ == "__main__":
    sample_text = "Git is fun. Git is fast!"
    print("Word count:", word_count(sample_text))
    print("Top 2 words:", top_k(sample_text, 2))
