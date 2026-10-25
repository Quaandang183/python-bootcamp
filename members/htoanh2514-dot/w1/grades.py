"""Module for computing statistical summary metrics from student grade lists."""

import statistics


def grade_summary(scores: list[float | int]) -> dict[str, float]:
    """Calculate basic statistical summary metrics for a list of numerical scores.

    Computes the minimum, maximum, arithmetic mean, and median values,
    rounded to 2 decimal places.

    Args:
        scores (list[float | int]): A list of numerical score values.

    Returns:
        dict[str, float]: A dictionary containing calculated metrics:
            - 'min': Minimum score value.
            - 'max': Maximum score value.
            - 'mean': Arithmetic mean of scores.
            - 'median': Median score value.

    Raises:
        ValueError: If the input scores list is empty.
    """
    if not scores:
        raise ValueError("List điểm số không được để trống.")

    min_val = round(min(scores), 2)
    max_val = round(max(scores), 2)
    mean_val = round(sum(scores) / len(scores), 2)
    median_val = round(statistics.median(scores), 2)

    return {
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "median": median_val,
    }