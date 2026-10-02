import numpy as np


def variance_threshold(x: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    """
    x: 2D float array (rows, columns)

    Returns:
        A boolean array of length `columns`: True where the column's
        population variance is strictly greater than `threshold`.
    """
    # TODO: Compare the per-column variance to the threshold.
    pass


def drop_correlated(x: np.ndarray, threshold: float) -> list:
    """
    Scans the columns left to right and keeps a column unless its
    absolute Pearson correlation with some already-kept column is
    strictly greater than `threshold`. A constant column has correlation
    0 with everything. Returns the sorted list of kept column indices.
    """
    # TODO: Standardize once, then compare each column to the kept ones.
    pass


def select_k_best(x: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    """
    Returns an int array of the k column indices with the highest absolute
    Pearson correlation with y, strongest first. Ties go to the lower
    index and a constant column scores 0.
    """
    # TODO: Score every column against y, then take the top k.
    pass
