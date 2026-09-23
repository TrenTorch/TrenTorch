import numpy as np


def sigmoid_forward(x: np.ndarray) -> np.ndarray:
    clipped = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-clipped))


def sigmoid_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    return grad_output * output * (1.0 - output)
