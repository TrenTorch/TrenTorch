import time

import numpy as np


def time_function(fn, num_runs: int = 5) -> list:
    times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        fn()
        end = time.perf_counter()
        times.append(end - start)
    return times


def benchmark_statistics(times: list) -> dict:
    times = np.asarray(times, dtype=float)
    return {
        "mean": float(times.mean()),
        "median": float(np.median(times)),
        "min": float(times.min()),
        "max": float(times.max()),
        "std": float(times.std()),
    }
