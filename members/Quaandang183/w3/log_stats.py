"""W3-2: statistics over chat-log (route, latency) pairs."""

import math
from collections import Counter, defaultdict


def percentile95(values: list[float]) -> float:
    """Return the 95th percentile (nearest-rank) of a non-empty list."""
    ordered = sorted(values)
    rank = math.ceil(0.95 * len(ordered))
    return ordered[rank - 1]


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Summarise ``(route, latency_ms)`` pairs.

    Returns ``{"counts": {route: n}, "p95": {route: ms}, "slowest": route}``.
    ``slowest`` is the route with the highest p95 (``None`` for empty input;
    ties go to the alphabetically first route).
    """
    counts = Counter(route for route, _ in pairs)
    latencies: defaultdict[str, list[float]] = defaultdict(list)
    for route, ms in pairs:
        latencies[route].append(ms)

    p95 = {route: percentile95(values) for route, values in latencies.items()}
    slowest = max(sorted(p95), key=p95.__getitem__) if p95 else None
    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
