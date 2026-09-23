import numpy as np


def leaky_relu_forward(x: np.ndarray, negative_slope: float = 0.01) -> np.ndarray:
    return np.where(x > 0.0, x, negative_slope * x)


def leaky_relu_backward(
    grad_output: np.ndarray, x: np.ndarray, negative_slope: float = 0.01
) -> np.ndarray:
    local_grad = np.where(x > 0.0, 1.0, negative_slope)
    return grad_output * local_grad
