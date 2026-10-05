import numpy as np


def explained_variance_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if np.all(y_true == y_true[0]):
        raise ValueError("y_true is constant, so the explained variance is undefined")
    return float(1.0 - np.var(y_true - y_pred) / np.var(y_true))
