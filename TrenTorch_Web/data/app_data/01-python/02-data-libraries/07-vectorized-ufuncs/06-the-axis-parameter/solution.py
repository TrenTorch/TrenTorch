import numpy as np


def sum_along_axis(arr: np.ndarray, axis: int) -> np.ndarray:
    return arr.sum(axis=axis)


def mean_keeping_dims(arr: np.ndarray, axis: int) -> np.ndarray:
    return arr.mean(axis=axis, keepdims=True)


def column_maxes(matrix: np.ndarray) -> np.ndarray:
    return matrix.max(axis=0)


def row_argmins(matrix: np.ndarray) -> np.ndarray:
    return matrix.argmin(axis=1)
