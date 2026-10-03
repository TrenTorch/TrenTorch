import numpy as np


def rbf_kernel(X: np.ndarray, Y: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    sq_x = np.sum(X * X, axis=1)[:, None]
    sq_y = np.sum(Y * Y, axis=1)[None, :]
    sq_dist = np.maximum(sq_x + sq_y - 2.0 * (X @ Y.T), 0.0)
    return np.exp(-gamma * sq_dist)
