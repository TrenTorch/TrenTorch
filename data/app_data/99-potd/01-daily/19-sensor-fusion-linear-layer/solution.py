import numpy as np


def linear_forward(W: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
    return W @ x + b
