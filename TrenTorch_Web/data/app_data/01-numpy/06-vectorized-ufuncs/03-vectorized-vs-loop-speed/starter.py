import time

import numpy as np


def multiply_with_loop(arr: np.ndarray, factor: float) -> np.ndarray:
    """
    Return a new array where every element of `arr` is multiplied
    by `factor`, computed using an explicit Python for loop
    (not vectorized). This exists to be timed against the
    vectorized version below.
    """
    pass


def multiply_vectorized(arr: np.ndarray, factor: float) -> np.ndarray:
    """
    Return a new array where every element of `arr` is multiplied
    by `factor`, using a single vectorized expression
    (arr * factor).
    """
    pass


def time_both_approaches(arr: np.ndarray, factor: float) -> dict:
    """
    Time both multiply_with_loop and multiply_vectorized on the
    same `arr` and `factor`, using time.time() (or time.perf_counter)
    before and after each call.

    Return a dictionary:
      {
        "loop_result": <result of multiply_with_loop>,
        "vectorized_result": <result of multiply_vectorized>,
        "loop_time_seconds": <float>,
        "vectorized_time_seconds": <float>,
        "vectorized_was_faster": <True if vectorized_time_seconds
            < loop_time_seconds>
      }
    """
    pass
