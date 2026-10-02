import numpy as np


def get_independent_slice(arr: np.ndarray, start: int, stop: int) -> np.ndarray:
    return arr[start:stop].copy()


def safe_modify_first_n(arr: np.ndarray, n: int, new_value) -> np.ndarray:
    result = arr.copy()
    result[:n] = new_value
    return result
