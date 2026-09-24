import numpy as np


def transpose_2d(arr: np.ndarray) -> np.ndarray:
    """
    Return the transpose of 2D array `arr` using .T.
    """
    pass


def transpose_axes(arr: np.ndarray, axes: tuple) -> np.ndarray:
    """
    Return `arr` with its axes reordered according to `axes`
    (a tuple giving the new order of axis positions), using
    .transpose(axes).
    """
    pass


def transpose_shares_memory(arr: np.ndarray) -> bool:
    """
    Return True if arr.T shares memory with arr, False
    otherwise, using np.shares_memory to check directly.
    """
    pass
