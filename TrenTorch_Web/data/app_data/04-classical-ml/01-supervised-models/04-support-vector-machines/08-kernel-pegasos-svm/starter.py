import numpy as np


def kernel_pegasos(K: np.ndarray, y: np.ndarray, lam: float = 0.1, iterations: int = 1000) -> np.ndarray:
    """
    Deterministic kernelized Pegasos. K is the (n, n) Gram matrix of the
    training points, y holds labels in {-1, +1}. At step t (from 1 to
    iterations), visit point i = (t - 1) % n and increment alpha[i] by
    1 when y[i] * decision < 1, where

        decision = sum_j alpha[j] * y[j] * K[j, i] / (lam * t)

    Returns alpha as a float array of shape (n,).
    """
    pass
