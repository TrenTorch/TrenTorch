import numpy as np


def mahalanobis(x: np.ndarray, y: np.ndarray, cov: np.ndarray) -> float:
    """
    sqrt((x - y)^T cov^-1 (x - y)). Raise ValueError for shape mismatches,
    a cov that is not symmetric, or a cov that is not positive definite.
    """
    pass
