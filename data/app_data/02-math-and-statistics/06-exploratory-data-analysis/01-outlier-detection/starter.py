import numpy as np


def detect_outliers_iqr(x: np.ndarray, k: float = 1.5) -> np.ndarray:
    """
    Flags values outside [Q1 - k*IQR, Q3 + k*IQR], where Q1/Q3 are the
    25th/75th percentiles and IQR = Q3 - Q1. Returns a boolean mask,
    same shape as x, True where a value is flagged as an outlier.
    """
    pass


def detect_outliers_zscore(x: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """
    Flags values whose z-score, (x - mean) / std, exceeds `threshold`
    in absolute value. Returns a boolean mask, same shape as x.
    """
    pass
