import numpy as np


def partial_derivative(f, x: np.ndarray, index: int, eps: float = 1e-5) -> float:
    x_plus = x.copy()
    x_plus[index] += eps
    x_minus = x.copy()
    x_minus[index] -= eps
    return (f(x_plus) - f(x_minus)) / (2 * eps)


def gradient(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    return np.array([partial_derivative(f, x, i, eps) for i in range(len(x))])
