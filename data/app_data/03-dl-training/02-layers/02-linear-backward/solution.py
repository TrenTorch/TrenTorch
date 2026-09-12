import numpy as np


def linear_backward(
    grad_output: np.ndarray, x: np.ndarray, weight: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    grad_x = grad_output @ weight
    grad_weight = grad_output.T @ x
    grad_bias = grad_output.sum(axis=0)
    return grad_x, grad_weight, grad_bias
