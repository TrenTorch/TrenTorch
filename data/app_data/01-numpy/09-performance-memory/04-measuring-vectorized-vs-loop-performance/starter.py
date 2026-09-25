import time

import numpy as np


def loop_sum_of_squares(values: list) -> int:
    """
    Return the sum of squares of the numbers in the Python list
    `values`, using an explicit Python for loop (no NumPy).
    Assume integer input.
    """
    pass


def vectorized_sum_of_squares(arr: np.ndarray) -> int:
    """
    Return the sum of squares of the elements of integer array `arr`,
    using vectorized NumPy operations only (no Python loop).
    """
    pass


def best_time(func, args: tuple, repeats: int) -> float:
    """
    Call func(*args) `repeats` times, timing each call with
    time.perf_counter(), and return the MINIMUM elapsed time in
    seconds as a float. `repeats` is at least 1.
    """
    pass


def benchmark_sum_of_squares(n: int, repeats: int = 3) -> dict:
    """
    Build the integers 0..n-1 as both a Python list and an integer
    ndarray (np.arange(n)). Measure both implementations with
    best_time. Return a dictionary:
      {
        "loop_time": <float, seconds>,
        "vec_time": <float, seconds>,
        "speedup": <float, loop_time / vec_time>,
        "results_match": <bool, True if both implementations return
                           the same value>
      }
    """
    pass
