"""Analysis module for request log latencies and counts."""

import math
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Any


def analyse(pairs: Iterable[tuple[str, float | int]]) -> dict[str, Any]:
    """Analyse request log pairs and compute route counts, p95 latency, and slowest route.

    Args:
        pairs: An iterable of (route, latency_ms) tuples.

    Returns:
        A dict containing:
        - "counts": Counter of requests per route
        - "p95": Dict mapping route to its 95th percentile latency (nearest-rank)
        - "slowest": The route with the highest p95 latency (or None if empty)
    """
    counts: Counter[str] = Counter()
    route_latencies: defaultdict[str, list[float | int]] = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        route_latencies[route].append(latency)

    p95: dict[str, float | int] = {}
    for route, latencies in route_latencies.items():
        sorted_lats = sorted(latencies)
        idx = math.ceil(0.95 * len(sorted_lats)) - 1
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=p95.get) if p95 else None

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
