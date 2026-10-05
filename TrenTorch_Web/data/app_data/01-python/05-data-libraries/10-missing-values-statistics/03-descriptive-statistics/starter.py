import numpy as np


def percentiles(a: np.ndarray, qs) -> np.ndarray:
    """The percentiles `qs` (each 0..100) of `a`, with linear interpolation."""
    # TODO: Interpolate between the sorted values.
    pass


def iqr(a: np.ndarray) -> float:
    """Interquartile range: 75th percentile minus 25th percentile."""
    # TODO: Difference of two percentiles.
    pass


def zscores(a: np.ndarray) -> np.ndarray:
    """(a - mean) / std with the population std (ddof=0); all zeros if the std is 0."""
    # TODO: Standardise, guarding against zero spread.
    pass


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation of two equal-length samples (do not call np.corrcoef)."""
    # TODO: Centre both samples, then use the formula.
    pass


def covariance_matrix(x: np.ndarray) -> np.ndarray:
    """Sample covariance (divide by n - 1) of the columns of 2D `x` (do not call np.cov)."""
    # TODO: Centre the columns and use one matrix product.
    pass
