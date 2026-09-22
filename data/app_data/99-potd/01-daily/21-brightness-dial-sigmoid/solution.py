import numpy as np


def sigmoid_forward(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    positive = np.where(x >= 0, x, 0.0)
    negative = np.where(x < 0, x, 0.0)

    sigma = np.where(
        x >= 0,
        1.0 / (1.0 + np.exp(-positive)),
        np.exp(negative) / (1.0 + np.exp(negative)),
    )
    grad = sigma * (1.0 - sigma)
    return sigma, grad
