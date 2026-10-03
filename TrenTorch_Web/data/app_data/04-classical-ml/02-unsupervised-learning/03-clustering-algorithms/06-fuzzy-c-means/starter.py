import numpy as np


def fuzzy_c_means(X: np.ndarray, c: int, m: float = 2.0, max_iter: int = 100, tol: float = 1e-5):
    """
    Fuzzy c-means clustering. Returns (centers, U) where centers is (c, d)
    and U is (n, c) with rows summing to 1. Raises ValueError when m <= 1
    or c is outside 1..n.
    """
    pass
