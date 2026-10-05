import numpy as np


def linear_kernel(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return X @ Y.T
