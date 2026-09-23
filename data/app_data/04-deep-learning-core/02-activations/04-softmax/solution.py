import numpy as np


def softmax_forward(x: np.ndarray) -> np.ndarray:
    shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_shifted = np.exp(shifted)
    return exp_shifted / np.sum(exp_shifted, axis=-1, keepdims=True)


def softmax_backward(grad_output: np.ndarray, output: np.ndarray) -> np.ndarray:
    dot = np.sum(grad_output * output, axis=-1, keepdims=True)
    return output * (grad_output - dot)
