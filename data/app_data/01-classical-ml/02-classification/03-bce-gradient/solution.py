import numpy as np


def bce_gradient(
    input: np.ndarray,
    p: np.ndarray,
    target: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    n_samples = input.shape[0]
    error = p - target
    grad_weight = (error.T @ input) / n_samples
    grad_bias = error.sum(axis=0) / n_samples
    return grad_weight, grad_bias
