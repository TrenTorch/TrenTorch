import numpy as np


def compute_summary(arr: np.ndarray) -> dict:
    return {
        "sum": arr.sum(),
        "mean": arr.mean(),
        "std": arr.std(),
        "min": arr.min(),
        "max": arr.max(),
        "argmin": arr.argmin(),
        "argmax": arr.argmax(),
    }


def sum_with_loop(arr: np.ndarray) -> float:
    total = 0
    for value in arr:
        total += value
    return total


def sum_along_axis(arr: np.ndarray, axis: int) -> np.ndarray:
    return arr.sum(axis=axis)


def mean_keeping_dims(arr: np.ndarray, axis: int) -> np.ndarray:
    return arr.mean(axis=axis, keepdims=True)


def column_maxes(matrix: np.ndarray) -> np.ndarray:
    return matrix.max(axis=0)


def row_argmins(matrix: np.ndarray) -> np.ndarray:
    return matrix.argmin(axis=1)
