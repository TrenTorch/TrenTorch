import numpy as np


def dropout_forward(x: np.ndarray, mask: np.ndarray, p: float) -> np.ndarray:
    return x * mask / (1.0 - p)


def dropout_backward(grad_output: np.ndarray, mask: np.ndarray, p: float) -> np.ndarray:
    return grad_output * mask / (1.0 - p)
