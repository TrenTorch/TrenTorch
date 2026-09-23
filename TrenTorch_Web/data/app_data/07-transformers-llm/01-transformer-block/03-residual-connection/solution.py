import numpy as np


def residual_connection(x: np.ndarray, sublayer_output: np.ndarray) -> np.ndarray:
    return x + sublayer_output


def residual_connection_backward(grad_output: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    grad_x = grad_output
    grad_sublayer_output = grad_output
    return grad_x, grad_sublayer_output
