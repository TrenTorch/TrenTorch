import numpy as np

from _load import load_solution

linear_kernel = load_solution("support-vector-machines-linear-kernel").linear_kernel


def polynomial_kernel(
    X: np.ndarray, Y: np.ndarray, degree: int = 3, coef0: float = 1.0, gamma: float = 1.0
) -> np.ndarray:
    return (gamma * linear_kernel(X, Y) + coef0) ** degree
