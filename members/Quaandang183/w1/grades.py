"""W1-1: summary statistics for a list of scores."""

from statistics import median


def summary(scores: list[float]) -> dict[str, float]:
    """Return min, max, mean and median (mean and median rounded to 2 places)."""
    if not scores:
        raise ValueError("scores must not be empty")
    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(median(scores), 2),
    }
