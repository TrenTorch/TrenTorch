import numpy as np


def normalize_rows(data: np.ndarray) -> np.ndarray:
    """
    Given a 2D array `data`, return a new array where each row
    has been normalized: (row - row_mean) / row_std, computed
    independently per row, using broadcasting (no explicit loop
    over rows).
    """
    pass


def pairwise_differences(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Given 1D arrays a (length n) and b (length m), return an
    (m, n) array where result[i, j] = a[j] - b[i], using
    broadcasting only.
    """
    pass


def scale_columns(matrix: np.ndarray, scale_factors: np.ndarray) -> np.ndarray:
    """
    Given a 2D matrix and a 1D scale_factors array whose length
    matches matrix's column count, return matrix with each
    column multiplied by its corresponding scale factor, using
    broadcasting.
    """
    pass
