import numpy as np


def _softplus(x: np.ndarray) -> np.ndarray:
    return np.logaddexp(0.0, x)


def _sigmoid(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-clipped))


def mish_forward(x: np.ndarray) -> np.ndarray:
    return x * np.tanh(_softplus(x))


def mish_backward(grad_output: np.ndarray, x: np.ndarray) -> np.ndarray:
    t = np.tanh(_softplus(x))
    s = _sigmoid(x)
    local_grad = t + x * (1.0 - t**2) * s
    return grad_output * local_grad
