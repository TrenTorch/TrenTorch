import numpy as np


def missing_mask(x: np.ndarray) -> np.ndarray:
    """
    Missing numeric values are represented as np.nan (NumPy/pandas'
    standard convention). Returns a boolean array the same shape as x,
    True wherever a value is missing.

    NOTE: `x == np.nan` is ALWAYS False, even for an actual NaN (NaN is
    defined to never equal anything, including itself), np.isnan is
    the correct tool here, not ==.
    """
    pass


def missing_count_per_column(x: np.ndarray) -> np.ndarray:
    """
    x is a 2D array, (rows, columns). Returns a length-`num_columns`
    array: how many missing values each column has.
    """
    pass


def missing_fraction_per_column(x: np.ndarray) -> np.ndarray:
    """
    Same as missing_count_per_column, but as a fraction of the total
    row count (0.0 to 1.0) rather than a raw count.
    """
    pass
