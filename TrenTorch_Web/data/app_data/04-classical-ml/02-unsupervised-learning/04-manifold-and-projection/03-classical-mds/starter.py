import numpy as np


def classical_mds(D: np.ndarray, k: int) -> np.ndarray:
    """
    Classical MDS coordinates of shape (n, k) from a distance matrix D.
    Raises ValueError when D is not a square symmetric matrix with zero
    diagonal, or when k is outside 1..n.
    """
    pass
