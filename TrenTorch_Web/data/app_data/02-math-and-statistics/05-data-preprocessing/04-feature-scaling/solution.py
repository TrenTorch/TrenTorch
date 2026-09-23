import numpy as np


def standardize(x: np.ndarray, mean: np.ndarray | None = None, std: np.ndarray | None = None):
    if mean is None:
        mean = np.mean(x, axis=0)
    if std is None:
        std = np.std(x, axis=0)
    return (x - mean) / std, mean, std


def min_max_normalize(
    x: np.ndarray, min_val: np.ndarray | None = None, max_val: np.ndarray | None = None
):
    if min_val is None:
        min_val = np.min(x, axis=0)
    if max_val is None:
        max_val = np.max(x, axis=0)
    return (x - min_val) / (max_val - min_val), min_val, max_val
