import numpy as np


def lle_weights(X: np.ndarray, k: int, reg: float = 1e-3) -> np.ndarray:
    """
    n by n reconstruction weights. Row i has k nonzero entries that sum to 1,
    on the k nearest neighbours of point i (self excluded).
    Raise ValueError if X is not 2-D or k is not in [1, n).
    """
    pass


def lle_embedding(W: np.ndarray, dim: int) -> np.ndarray:
    """
    n by dim embedding from the eigenvectors of (I - W)^T (I - W) with
    eigenvalues ranked 2nd through (dim + 1)th. Raise ValueError for a
    non-square W or dim not in [1, n).
    """
    pass
