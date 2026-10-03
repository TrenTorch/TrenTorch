import numpy as np

from _load import load_solution

linear_kernel = load_solution("support-vector-machines-linear-kernel").linear_kernel


def sigmoid_kernel(X: np.ndarray, Y: np.ndarray, gamma: float = 1.0, coef0: float = 0.0) -> np.ndarray:
    """
    Sigmoid similarity between the rows of X (shape (n, d)) and the
    rows of Y (shape (m, d)). Returns an array of shape (n, m) where
    entry [i, j] is tanh(gamma * X[i] @ Y[j] + coef0).
    """
    pass
