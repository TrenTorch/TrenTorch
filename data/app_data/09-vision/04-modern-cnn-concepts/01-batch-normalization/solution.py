import numpy as np


def batch_norm2d(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    mean = x.mean(axis=(0, 2, 3), keepdims=True)
    var = x.var(axis=(0, 2, 3), keepdims=True)
    x_norm = (x - mean) / np.sqrt(var + eps)
    gamma_r = gamma.reshape(1, -1, 1, 1)
    beta_r = beta.reshape(1, -1, 1, 1)
    return gamma_r * x_norm + beta_r
