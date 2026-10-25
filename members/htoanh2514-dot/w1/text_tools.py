"""Module for text processing tools including word frequency counting and ranking."""

import re
from collections import Counter


def word_count(text: str) -> Counter:
    """Count word frequencies in a text string, ignoring punctuation and case sensitivity.

    Args:
        text (str): The input text string to analyze.

    Returns:
        Counter: A Counter mapping normalized lowercase words to their frequencies.
    """
    # Convert text to lowercase for case-insensitive matching
    text = text.lower()
    # Strip basic punctuation marks (, . ! ? ; :)
    text = re.sub(r"[,.!?;:]", "", text)
    # Split string by whitespace into words
    words = text.split()
    # Return word frequency counter
    return Counter(words)


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Retrieve the top-K most frequent words from a given text.

    Sorts candidates primarily by frequency in descending order, and secondarily
    by alphabetical order (ascending) in case of ties.

    Args:
        text (str): The input text string to analyze.
        k (int): The number of top entries to return.

    Returns:
        list[tuple[str, int]]: A list of tuples containing (word, frequency) up to K elements.
    """
    counter = word_count(text)
    # Sort primarily by count descending (-item[1]), secondarily by word ascending (item[0])
    sorted_words = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:k]