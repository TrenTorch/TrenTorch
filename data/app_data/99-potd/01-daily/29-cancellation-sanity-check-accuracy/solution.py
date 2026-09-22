import numpy as np


def accuracy(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean(p == y))
