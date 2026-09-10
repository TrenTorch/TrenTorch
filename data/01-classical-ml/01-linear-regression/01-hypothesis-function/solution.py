import numpy as np


def linear_forward(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    return X @ w + b
