"""Module for computing statistical summary metrics from student grade lists."""

import statistics


def summary(scores: list[float]) -> dict:
    """Calculate statistical summary (min, max, mean, median) for a list of scores.

    Args:
        scores: A list of numerical score values.

    Returns:
        A dictionary containing "min", "max", "mean", and "median" values.

    Raises:
        ValueError: If scores list is empty.
    """
    if not scores:
        raise ValueError("List is empty")

    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(statistics.median(scores), 2),
    }

