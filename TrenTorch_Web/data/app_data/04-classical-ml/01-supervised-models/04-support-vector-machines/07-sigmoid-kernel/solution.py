import numpy as np

from _load import load_solution

linear_kernel = load_solution("support-vector-machines-linear-kernel").linear_kernel


def sigmoid_kernel(X: np.ndarray, Y: np.ndarray, gamma: float = 1.0, coef0: float = 0.0) -> np.ndarray:
    return np.tanh(gamma * linear_kernel(X, Y) + coef0)
