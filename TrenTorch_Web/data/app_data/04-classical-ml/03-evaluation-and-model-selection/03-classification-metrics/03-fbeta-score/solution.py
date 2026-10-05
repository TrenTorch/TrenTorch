import numpy as np


def fbeta_score(y_true: np.ndarray, y_pred: np.ndarray, beta: float = 1.0, positive=1) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    if beta <= 0:
        raise ValueError("beta must be greater than zero")
    actual = y_true == positive
    predicted = y_pred == positive
    tp = np.sum(actual & predicted)
    fp = np.sum(~actual & predicted)
    fn = np.sum(actual & ~predicted)
    precision = tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = tp / (tp + fn) if tp + fn > 0 else 0.0
    b2 = beta ** 2
    denom = b2 * precision + recall
    if denom == 0:
        return 0.0
    return float((1 + b2) * precision * recall / denom)
