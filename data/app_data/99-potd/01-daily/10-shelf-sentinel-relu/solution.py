import numpy as np


def relu_forward(x: np.ndarray, g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mask = x > 0
    activated = np.where(mask, x, 0.0)
    grad = g * mask
    return activated, grad
