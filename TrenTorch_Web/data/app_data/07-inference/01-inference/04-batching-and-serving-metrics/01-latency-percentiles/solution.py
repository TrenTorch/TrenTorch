import numpy as np


def _percentile(sorted_arr, p):
    n = len(sorted_arr)
    if n == 1:
        return float(sorted_arr[0])
    rank = (p / 100.0) * (n - 1)
    lo = int(np.floor(rank))
    hi = min(lo + 1, n - 1)
    frac = rank - lo
    return float(sorted_arr[lo] + frac * (sorted_arr[hi] - sorted_arr[lo]))


def latency_percentiles(latencies: list, percentiles: tuple = (50, 95, 99)) -> dict:
    arr = np.sort(np.array(latencies, dtype=float))
    return {f"p{p}": _percentile(arr, p) for p in percentiles}
