import numpy as np


def compute_summary(arr: np.ndarray) -> dict:
    """
    Return a dictionary with keys "sum", "mean", "std", "min",
    "max", "argmin", "argmax", each computed using the
    corresponding NumPy aggregation method on `arr` (assume arr
    is 1D for this function).
    """
    pass


def sum_with_loop(arr: np.ndarray) -> float:
    """
    Compute and return the sum of all elements in `arr` using an
    explicit Python for loop (not arr.sum()), to be compared
    against the vectorized version.
    """
    pass


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
