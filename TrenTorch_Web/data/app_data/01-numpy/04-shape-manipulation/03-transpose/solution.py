import numpy as np


def transpose_2d(arr: np.ndarray) -> np.ndarray:
    return arr.T


def transpose_axes(arr: np.ndarray, axes: tuple) -> np.ndarray:
    return arr.transpose(axes)


def transpose_shares_memory(arr: np.ndarray) -> bool:
    return bool(np.shares_memory(arr, arr.T))
