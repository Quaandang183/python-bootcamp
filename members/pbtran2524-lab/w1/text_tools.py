import re
from collections import Counter


def clean_text(text: str) -> list[str]:
    cleaned = re.sub(r"[,.!?/;:\"'()\[\]{}]", "", text.lower())
    return cleaned.split()


def word_count(text: str) -> dict[str, int]:
    words = clean_text(text)
    return dict(Counter(words))


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:k]