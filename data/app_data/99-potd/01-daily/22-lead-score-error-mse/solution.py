import numpy as np


def mse(y: np.ndarray, yhat: np.ndarray) -> float:
    diff = y - yhat
    return float(np.mean(diff**2))
