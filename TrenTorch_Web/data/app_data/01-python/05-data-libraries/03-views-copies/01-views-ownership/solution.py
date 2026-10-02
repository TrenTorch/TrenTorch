import numpy as np


def is_view_of(candidate: np.ndarray, source: np.ndarray) -> bool:
    return bool(np.shares_memory(candidate, source))


def owns_its_data(arr: np.ndarray) -> bool:
    return arr.base is None


def find_ultimate_owner(arr: np.ndarray) -> np.ndarray:
    current = arr
    while current.base is not None:
        current = current.base
    return current
