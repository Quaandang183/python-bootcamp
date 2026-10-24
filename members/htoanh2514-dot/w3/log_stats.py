"""Module for analyzing service log execution statistics."""

from collections import defaultdict
import math
from typing import Any, Sequence


def _calculate_p95(values: Sequence[float | int]) -> float | int:
    """Calculate the 95th percentile value using nearest rank method."""
    if not values:
        return 0
    sorted_values = sorted(values)
    index = math.ceil(0.95 * len(sorted_values)) - 1
    return sorted_values[max(0, index)]


def analyse(pairs: list[tuple[str, float | int]]) -> dict[str, Any]:
    """Analyze service log duration records.

    Args:
        pairs: List of tuples containing (service_name, duration_ms).

    Returns:
        A dictionary containing:
        - 'counts': Count of requests per service.
        - 'slowest': Service with the highest average execution time.
        - 'p95': 95th percentile latency per service.
    """
    if not pairs:
        return {"counts": {}, "slowest": None, "p95": {}}

    groups = defaultdict(list)
    counts = defaultdict(int)

    for service, duration in pairs:
        groups[service].append(duration)
        counts[service] += 1

    p95_dict = {}
    highest_avg = -1.0
    slowest_service = None

    for service, durations in groups.items():
        avg_duration = sum(durations) / len(durations)
        if avg_duration > highest_avg:
            highest_avg = avg_duration
            slowest_service = service

        p95_dict[service] = _calculate_p95(durations)

    return {
        "counts": dict(counts),
        "slowest": slowest_service,
        "p95": p95_dict,
    }