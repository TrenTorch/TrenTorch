import numpy as np


def specificity(y_true: np.ndarray, y_pred: np.ndarray, positive=1) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    negatives = y_true != positive
    if not np.any(negatives):
        return 0.0
    return float(np.mean(y_pred[negatives] != positive))
