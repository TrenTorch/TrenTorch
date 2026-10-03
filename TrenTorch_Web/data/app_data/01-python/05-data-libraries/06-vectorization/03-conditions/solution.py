import numpy as np


def in_range_mask(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    return (arr > low) & (arr < high)


def outside_range_mask(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    return (arr < low) | (arr > high)


def not_matching(arr: np.ndarray, value: float) -> np.ndarray:
    return ~(arr == value)
