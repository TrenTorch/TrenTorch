import numpy as np


def matthews_corrcoef(y_true: np.ndarray, y_pred: np.ndarray, positive=1) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    actual = y_true == positive
    predicted = y_pred == positive
    tp = float(np.sum(actual & predicted))
    tn = float(np.sum(~actual & ~predicted))
    fp = float(np.sum(~actual & predicted))
    fn = float(np.sum(actual & ~predicted))
    denom = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return 0.0
    return float((tp * tn - fp * fn) / denom)
