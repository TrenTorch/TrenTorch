import numpy as np


def tanh_forward(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


def tanh_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    return grad_output * (1.0 - output**2)
