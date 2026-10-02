import numpy as np


def select_above_threshold(arr: np.ndarray, threshold: float) -> np.ndarray:
    return arr[arr > threshold]


def select_in_range(arr: np.ndarray, low: float, high: float) -> np.ndarray:
    return arr[(arr > low) & (arr < high)]


def zero_out_negatives(arr: np.ndarray) -> None:
    arr[arr < 0] = 0


def find_indices_above(arr: np.ndarray, threshold: float) -> np.ndarray:
    return np.where(arr > threshold)[0]


def replace_above_threshold(arr: np.ndarray, threshold: float, replacement) -> np.ndarray:
    return np.where(arr > threshold, replacement, arr)


def sign_labels(arr: np.ndarray) -> np.ndarray:
    return np.where(arr > 0, "positive", "non-positive")
