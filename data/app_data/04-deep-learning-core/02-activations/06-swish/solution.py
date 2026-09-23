import numpy as np


def _sigmoid(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-clipped))


def swish_forward(x: np.ndarray) -> np.ndarray:
    return x * _sigmoid(x)


def swish_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    s = _sigmoid(x)
    local_grad = s + x * s * (1.0 - s)
    return grad_output * local_grad
