import math
from collections import Counter, defaultdict


def calculate_p95(latencies: list[float]) -> float:
    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    # CÔNG THỨC PERCENTILE 95 NEAREST-RANK
    index = math.ceil(0.95 * n) - 1
    return float(sorted_latencies[max(0, index)])

def analyse(pairs: list[tuple[str, float]]) -> dict:
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