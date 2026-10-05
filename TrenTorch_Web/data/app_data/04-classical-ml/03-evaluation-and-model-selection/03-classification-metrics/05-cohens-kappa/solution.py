import numpy as np


def cohens_kappa(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    if y_true.size == 0:
        raise ValueError("inputs are empty")
    p_o = np.mean(y_true == y_pred)
    labels = np.unique(np.concatenate([y_true, y_pred]))
    p_e = sum(np.mean(y_true == c) * np.mean(y_pred == c) for c in labels)
    if np.isclose(p_e, 1.0):
        return 1.0
    return float((p_o - p_e) / (1.0 - p_e))
