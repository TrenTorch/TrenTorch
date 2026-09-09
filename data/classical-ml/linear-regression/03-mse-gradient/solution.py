import numpy as np


def mse_grad(X: np.ndarray, y_hat: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    n = X.shape[0]
    error = y_hat - y
    dw = (2 / n) * X.T @ error
    db = (2 / n) * np.sum(error)
    return dw, float(db)
