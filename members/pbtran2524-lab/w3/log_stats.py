"""Latency analysis utility module.

This module provides functions to process API/service route latency data,
compute the 95th percentile (P95) latency using the nearest-rank method,
and analyze route request distributions.
"""

import math
from collections import Counter, defaultdict


def calculate_p95(latencies: list[float]) -> float:
    """Calculate the 95th percentile (P95) latency using nearest-rank method.

    Args:
        latencies (list[float]): A list of measured latency values in seconds or milliseconds.

    Returns:
        float: The 95th percentile latency value. Returns 0.0 if the input list is empty.
    """
    if not latencies:
        return 0.0

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    # CÔNG THỨC PERCENTILE 95 NEAREST-RANK
    index = math.ceil(0.95 * n) - 1
    return float(sorted_latencies[max(0, index)])


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Analyze request counts, P95 latency per route, and identify the slowest route.

    Args:
        pairs (list[tuple[str, float]]): A list of tuples where each tuple contains
            the route identifier (str) and its observed latency value (float).

    Returns:
        dict: A summary dictionary with three key-value pairs:
            - 'counts' (dict[str, int]): Total request count per route.
            - 'p95' (dict[str, float]): Calculated 95th percentile latency per route.
            - 'slowest' (str | None): The route name with the highest P95 latency,
              or None if the input pairs list is empty.
    """
    if not pairs:
        return {"counts": {}, "p95": {}, "slowest": None}

    counts = Counter()
    route_latencies = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        route_latencies[route].append(latency)

    p95_dict = {}
    for route, latencies in route_latencies.items():
        p95_dict[route] = calculate_p95(latencies)

    # Tìm route có p95 cao nhất
    slowest_route = max(p95_dict, key=p95_dict.get) if p95_dict else None

    return {
        "counts": dict(counts),
        "p95": p95_dict,
        "slowest": slowest_route
    }