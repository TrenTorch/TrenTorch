import time

import numpy as np


def multiply_with_loop(arr: np.ndarray, factor: float) -> np.ndarray:
    result = np.empty_like(arr, dtype=float)
    for i in range(len(arr)):
        result[i] = arr[i] * factor
    return result


def multiply_vectorized(arr: np.ndarray, factor: float) -> np.ndarray:
    return arr * factor


def time_both_approaches(arr: np.ndarray, factor: float) -> dict:
    start = time.perf_counter()
    loop_result = multiply_with_loop(arr, factor)
    loop_time_seconds = time.perf_counter() - start

    start = time.perf_counter()
    vectorized_result = multiply_vectorized(arr, factor)
    vectorized_time_seconds = time.perf_counter() - start

    return {
        "loop_result": loop_result,
        "vectorized_result": vectorized_result,
        "loop_time_seconds": loop_time_seconds,
        "vectorized_time_seconds": vectorized_time_seconds,
        "vectorized_was_faster": vectorized_time_seconds < loop_time_seconds,
    }
