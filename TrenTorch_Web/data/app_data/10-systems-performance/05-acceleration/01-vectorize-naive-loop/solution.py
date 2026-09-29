import time

import numpy as np


def naive_dot_product(a: list, b: list) -> float:
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def vectorized_dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def compare_speed(a: np.ndarray, b: np.ndarray) -> dict:
    a_list, b_list = a.tolist(), b.tolist()

    start = time.perf_counter()
    naive_result = naive_dot_product(a_list, b_list)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    vectorized_result = vectorized_dot_product(a, b)
    vectorized_time = time.perf_counter() - start

    return {
        "naive_result": naive_result,
        "vectorized_result": vectorized_result,
        "naive_time": naive_time,
        "vectorized_time": vectorized_time,
        "speedup": naive_time / vectorized_time if vectorized_time > 0 else float("inf"),
    }
