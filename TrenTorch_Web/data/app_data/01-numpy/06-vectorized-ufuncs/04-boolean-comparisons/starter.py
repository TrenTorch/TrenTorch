import numpy as np


def in_range_mask(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    """
    Return a boolean array the same shape as `arr`, True at
    positions where the value is strictly between `low` and
    `high`, using & to combine two comparisons.
    """
    pass


def outside_range_mask(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    """
    Return a boolean array the same shape as `arr`, True at
    positions where the value is less than `low` OR greater than
    `high`, using |.
    """
    pass


def not_matching(arr: np.ndarray, value: float) -> np.ndarray:
    """
    Return a boolean array the same shape as `arr`, True at every
    position where the value does NOT equal `value`, using ~.
    """
    pass
