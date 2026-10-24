"""Chat log latency analysis module."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from math import ceil


def analyse(pairs: Iterable[tuple[str, float | int]]) -> dict:
    """Analyse chat log route latencies.

    Args:
        pairs: Iterable of (route, latency_ms) tuples.

    Returns:
        dict: A dictionary containing:
            - "counts": Request counts per route (Counter).
            - "p95": 95th percentile latency per route (nearest-rank).
            - "slowest": Route name with the highest p95 latency.
    """
    groups: dict[str, list[float]] = defaultdict(list)
    counts: Counter[str] = Counter()

    for route, latency in pairs:
        counts[route] += 1
        groups[route].append(float(latency))

    p95: dict[str, float | int] = {}
    for route, latencies in groups.items():
        sorted_latencies = sorted(latencies)
        idx = ceil(0.95 * len(sorted_latencies)) - 1
        idx = max(0, min(idx, len(sorted_latencies) - 1))
        # Keep as int if it was originally whole number / int
        val = sorted_latencies[idx]
        p95[route] = int(val) if isinstance(val, float) and val.is_integer() else val

    slowest = max(p95, key=lambda r: p95[r]) if p95 else None

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
