import numpy as np


def insertion_points(sorted_a: np.ndarray, values: np.ndarray, side: str) -> np.ndarray:
    return np.searchsorted(sorted_a, values, side=side)


def count_between(sorted_a: np.ndarray, lo, hi) -> int:
    return int(np.searchsorted(sorted_a, hi, side="right") - np.searchsorted(sorted_a, lo, side="left"))


def bucketize(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    return np.searchsorted(edges, values, side="right")


def nearest_value(sorted_a: np.ndarray, targets: np.ndarray) -> np.ndarray:
    sorted_a = np.asarray(sorted_a)
    targets = np.asarray(targets)
    i = np.searchsorted(sorted_a, targets, side="left")
    lower = sorted_a[np.clip(i - 1, 0, len(sorted_a) - 1)]
    upper = sorted_a[np.clip(i, 0, len(sorted_a) - 1)]
    return np.where(np.abs(targets - lower) <= np.abs(upper - targets), lower, upper)


def is_present(sorted_a: np.ndarray, values: np.ndarray) -> np.ndarray:
    sorted_a = np.asarray(sorted_a)
    values = np.asarray(values)
    i = np.clip(np.searchsorted(sorted_a, values, side="left"), 0, len(sorted_a) - 1)
    return sorted_a[i] == values
