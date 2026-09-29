import numpy as np


def relu_forward(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)


def relu_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    return grad_output * (x > 0).astype(grad_output.dtype)
