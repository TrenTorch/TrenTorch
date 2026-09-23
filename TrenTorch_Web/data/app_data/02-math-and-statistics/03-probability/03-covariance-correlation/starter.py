import numpy as np


def covariance(x: np.ndarray, y: np.ndarray, ddof: int = 0) -> float:
    """
    Covariance measures whether x and y tend to move together (positive),
    move oppositely (negative), or show no consistent relationship
    (near zero):

        cov(x, y) = (1/(n - ddof)) * sum((x_i - mean(x)) * (y_i - mean(y)))

    Same ddof convention 02-expectation-variance's sample_variance uses
    (in fact, covariance(x, x, ddof) is exactly sample_variance(x, ddof)).
    """
    pass


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    """
    Correlation rescales covariance into a unitless number in [-1, 1],
    by dividing out each variable's own spread:

        corr(x, y) = cov(x, y) / (std(x) * std(y))
    """
    pass
