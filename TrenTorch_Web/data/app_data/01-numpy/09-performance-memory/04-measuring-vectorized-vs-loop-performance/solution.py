import time

import numpy as np


def loop_sum_of_squares(values: list) -> int:
    total = 0
    for v in values:
        total += v * v
    return total


def vectorized_sum_of_squares(arr: np.ndarray) -> int:
    return (arr * arr).sum()


def best_time(func, args: tuple, repeats: int) -> float:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        times.append(time.perf_counter() - start)
    return min(times)


def benchmark_sum_of_squares(n: int, repeats: int = 3) -> dict:
    values = list(range(n))
    arr = np.arange(n)

    loop_time = best_time(loop_sum_of_squares, (values,), repeats)
    vec_time = best_time(vectorized_sum_of_squares, (arr,), repeats)

    results_match = loop_sum_of_squares(values) == vectorized_sum_of_squares(arr)

    return {
        "loop_time": loop_time,
        "vec_time": vec_time,
        "speedup": loop_time / vec_time,
        "results_match": bool(results_match),
    }
