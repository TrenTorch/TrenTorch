import numpy as np


def bce_grad(X: np.ndarray, p: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    n = X.shape[0]
    error = p - y
    dw = (1 / n) * X.T @ error
    db = (1 / n) * np.sum(error)
    return dw, float(db)
