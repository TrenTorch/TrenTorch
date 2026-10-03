import numpy as np


def detect_outliers_iqr(x: np.ndarray, k: float = 1.5) -> np.ndarray:
    q1 = np.percentile(x, 25)
    q3 = np.percentile(x, 75)
    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    return (x < lower_bound) | (x > upper_bound)


def detect_outliers_zscore(x: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    z_scores = (x - np.mean(x)) / np.std(x)
    return np.abs(z_scores) > threshold
