"""Student grades analysis utilities."""

import statistics


def summary(scores: list[float]) -> dict[str, float]:
    """Calculate statistical summary (min, max, mean, median) for a list of scores.

    Args:
        scores: A list of numeric score values.

    Returns:
        A dictionary containing "min", "max", "mean", and "median" rounded to 2 decimals.

    Raises:
        ValueError: If scores list is empty.
    """
    if not scores:
        raise ValueError("Danh sách điểm số không được để trống!")

    return {
        "min": round(float(min(scores)), 2),
        "max": round(float(max(scores)), 2),
        "mean": round(float(sum(scores) / len(scores)), 2),
        "median": round(float(statistics.median(scores)), 2),
    }


grade_sum = summary

if __name__ == "__main__":
    scores_list = [8.5, 9.0, 7.5, 6.0, 8.0]
    print("Kết quả:", summary(scores_list))