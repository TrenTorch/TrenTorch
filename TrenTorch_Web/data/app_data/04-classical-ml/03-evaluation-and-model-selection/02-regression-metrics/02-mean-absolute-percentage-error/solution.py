import numpy as np


def mean_absolute_percentage_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if np.any(y_true == 0):
        raise ValueError("y_true contains zero, so the percentage error is undefined")
    return float(100.0 * np.mean(np.abs(y_true - y_pred) / np.abs(y_true)))
