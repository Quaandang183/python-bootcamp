"""Text processing and word frequency analysis module.

This module provides utilities to normalize raw text, calculate word counts,
and retrieve the top-K most frequent words with deterministic tie-breaking.
"""

import re
from collections import Counter


def clean_text(text: str) -> list[str]:
    """Normalize input text by lowercasing and removing punctuation marks.

    Args:
        text (str): The raw text string to normalize.

    Returns:
        list[str]: A list of cleaned, individual word tokens.
    """
    cleaned = re.sub(r"[,.!?/;:\"'()\[\]{}]", "", text.lower())
    return cleaned.split()


def word_count(text: str) -> dict[str, int]:
    """Count the occurrence frequency of each word in the provided text.

    Args:
        text (str): The raw text string to analyze.

    Returns:
        dict[str, int]: A dictionary mapping each unique word to its frequency count.
    """
    words = clean_text(text)
    return dict(Counter(words))


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Retrieve the top-K most frequent words with deterministic sorting.

    Words are sorted primarily by frequency in descending order. Ties in frequency
    are broken alphabetically in ascending order.

    Args:
        text (str): The raw text string to analyze.
        k (int): The maximum number of top words to return.

    Returns:
        list[tuple[str, int]]: A list of tuples containing (word, count) pairs,
            limited to the top `k` results.
    """
    counts = word_count(text)
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:k]