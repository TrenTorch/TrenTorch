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


def find_indices_above(arr: np.ndarray, threshold: float) -> np.ndarray:
    """
    Return a 1D array of the indices in `arr` where the value is
    strictly greater than `threshold`, using np.where's
    one-argument form. (arr is guaranteed to be 1D.)
    """
    pass


def replace_above_threshold(arr: np.ndarray, threshold: float, replacement) -> np.ndarray:
    """
    Return a new array the same shape as `arr`, where every
    element greater than `threshold` is replaced with
    `replacement`, and every other element keeps its original
    value from `arr`. Use np.where's three-argument form.
    Do not mutate `arr` itself.
    """
    pass


def sign_labels(arr: np.ndarray) -> np.ndarray:
    """
    Return a new array of the same shape as `arr`, where each
    element is the string "positive" if the corresponding
    element in `arr` is greater than 0, and "non-positive"
    otherwise. Use np.where.
    """
    pass
