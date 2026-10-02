import numpy as np


def select_above_threshold(arr: np.ndarray, threshold: float) -> np.ndarray:
    """
    Return a new array containing only the elements of `arr`
    that are strictly greater than `threshold`, using boolean
    masking (not a loop).
    """
    pass


def select_in_range(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    """
    Return a new array containing only the elements of `arr`
    that are strictly between `low` and `high` (exclusive on
    both ends), using a combined boolean mask.
    """
    pass


def zero_out_negatives(arr: np.ndarray) -> None:
    """
    Mutate `arr` in place so that every negative element becomes
    0, using boolean mask assignment. Do not return anything,
    and do not reassign `arr` to a new array.
    """
    pass
