import numpy as np


def find_indices_above(arr: np.ndarray, threshold: float) -> np.ndarray:
    return np.where(arr > threshold)[0]


def replace_above_threshold(arr: np.ndarray, threshold: float, replacement) -> np.ndarray:
    return np.where(arr > threshold, replacement, arr)


def sign_labels(arr: np.ndarray) -> np.ndarray:
    return np.where(arr > 0, "positive", "non-positive")
