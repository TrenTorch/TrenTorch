import numpy as np


def summary_ignoring_nan(a: np.ndarray) -> dict:
    """
    {"count", "mean", "std", "min", "max"} over the non-NaN values of the 1D array
    `a` (std with ddof=0). If there are no known values: count 0 and NaN for the rest.
    """
    # TODO: Use the nan-aware functions.
    pass


def count_missing(m: np.ndarray, axis: int) -> np.ndarray:
    """Number of NaN entries along `axis` of `m`."""
    # TODO: Count the NaNs.
    pass


def fill_with_column_means(m: np.ndarray) -> np.ndarray:
    """
    Copy of 2D `m` with every NaN replaced by the mean of the non-NaN values of its
    column (0.0 for a column that is entirely NaN). `m` is not changed.
    """
    # TODO: Column means over the known values, then fill the holes.
    pass


def rows_without_nan(m: np.ndarray) -> np.ndarray:
    """The rows of 2D `m` that contain no NaN, in their original order."""
    # TODO: Mask the incomplete rows.
    pass


def argmax_ignoring_nan(a: np.ndarray) -> int:
    """Index of the largest non-NaN value of 1D `a`; -1 if every value is NaN."""
    # TODO: Ignore the holes.
    pass
