import numpy as np


def latency_percentiles(latencies: list, percentiles: tuple = (50, 95, 99)) -> dict:
    """
    latencies: list of per-request latency measurements.
    percentiles: which percentiles to compute (0-100 each).

    Returns a dict like {"p50": ..., "p95": ..., "p99": ...}.
    """
    # TODO: Sort latencies, then for each requested percentile compute
    # rank = p/100 * (n-1) and linearly interpolate between the two
    # bracketing sorted samples. Handle n == 1 as a special case.
    pass
