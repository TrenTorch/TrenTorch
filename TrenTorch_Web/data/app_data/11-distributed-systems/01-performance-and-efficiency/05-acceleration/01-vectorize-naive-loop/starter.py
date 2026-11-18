import time

import numpy as np


def naive_dot_product(a: list, b: list) -> float:
    """
    a, b: plain Python lists of equal length

    The dot product computed the way anyone would first write it in
    plain Python: a loop, one multiply-add at a time.
    """
    # TODO: sum(x * y for x, y in zip(a, b)), or an equivalent explicit
    # loop with a running total.
    pass


def vectorized_dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    a, b: NumPy arrays of equal length

    The same dot product, expressed as a single vectorized NumPy
    operation instead of a Python-level loop.
    """
    # TODO: np.dot(a, b), cast to a plain float.
    pass


def compare_speed(a: np.ndarray, b: np.ndarray) -> dict:
    """
    a, b: NumPy arrays of equal length

    Runs BOTH implementations on the same data, times each with
    time.perf_counter(), and reports both results and both timings so
    the speedup can actually be measured, not assumed.

    Returns: {"naive_result": ..., "vectorized_result": ...,
              "naive_time": ..., "vectorized_time": ..., "speedup": ...}
    """
    # TODO: convert a/b to plain lists with .tolist() for
    # naive_dot_product (it expects lists, not arrays). Time each call
    # around it with time.perf_counter() before/after. speedup =
    # naive_time / vectorized_time.
    pass
