import numpy as np


def sum_along_axis(arr: np.ndarray, axis: int) -> np.ndarray:
    """
    Return the sum of `arr` along the given `axis`, using
    arr.sum(axis=axis).
    """
    pass


def mean_keeping_dims(arr: np.ndarray, axis: int) -> np.ndarray:
    """
    Return the mean of `arr` along the given `axis`, using
    keepdims=True so the result retains that axis as a size-1
    dimension rather than removing it.
    """
    pass


def column_maxes(matrix: np.ndarray) -> np.ndarray:
    """
    Given a 2D matrix, return a 1D array containing the maximum
    value of each column (i.e. aggregate along the row axis).
    """
    pass


def row_argmins(matrix: np.ndarray) -> np.ndarray:
    """
    Given a 2D matrix, return a 1D array containing, for each
    row, the column index of that row's minimum value.
    """
    pass
