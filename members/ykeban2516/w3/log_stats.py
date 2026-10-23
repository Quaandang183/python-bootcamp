"""Summarize request counts and latency by intent."""

from collections import defaultdict
from collections.abc import Iterable
from math import ceil, isfinite


def analyse(pairs: Iterable[tuple[str, float]]) -> dict:
    """Use nearest-rank P95 and mean latency to identify the slowest intent."""
    groups = defaultdict(list)
    for intent, latency in pairs:
        if not isinstance(intent, str) or not intent.strip():
            raise ValueError("Intent must be a nonempty string")
        if (
            isinstance(latency, bool)
            or not isinstance(latency, (int, float))
            or not isfinite(latency)
            or latency < 0
        ):
            raise ValueError("Latency must be finite and nonnegative")
        groups[intent].append(latency)

    counts = {intent: len(values) for intent, values in groups.items()}
    p95 = {
        intent: sorted(values)[ceil(0.95 * len(values)) - 1]
        for intent, values in groups.items()
    }
    slowest = max(
        groups,
        key=lambda intent: sum(groups[intent]) / len(groups[intent]),
        default=None,
    )
    return {"counts": counts, "p95": p95, "slowest": slowest}
