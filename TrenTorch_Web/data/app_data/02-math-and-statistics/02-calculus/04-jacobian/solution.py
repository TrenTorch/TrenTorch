import numpy as np


def jacobian(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    n = len(x)
    output_size = len(np.atleast_1d(f(x)))
    result = np.zeros((output_size, n))
    for j in range(n):
        x_plus = x.copy()
        x_plus[j] += eps
        x_minus = x.copy()
        x_minus[j] -= eps
        result[:, j] = (np.atleast_1d(f(x_plus)) - np.atleast_1d(f(x_minus))) / (2 * eps)
    return result
