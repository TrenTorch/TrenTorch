import numpy as np


def mse_loss(y_hat: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((y_hat - y) ** 2))
