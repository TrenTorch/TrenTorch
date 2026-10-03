import numpy as np


def hamming_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if y_true.size == 0:
        raise ValueError("inputs are empty")
    return float(np.mean(y_true != y_pred))
