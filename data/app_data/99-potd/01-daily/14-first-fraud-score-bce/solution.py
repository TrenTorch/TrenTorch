import numpy as np


def bce_loss(y: np.ndarray, yhat: np.ndarray) -> float:
    terms = y * np.log(yhat) + (1 - y) * np.log(1 - yhat)
    return float(-np.mean(terms))
