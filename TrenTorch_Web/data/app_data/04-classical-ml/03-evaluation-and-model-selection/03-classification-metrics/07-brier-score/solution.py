import numpy as np


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_prob = np.asarray(y_prob, dtype=float)
    if y_true.shape != y_prob.shape:
        raise ValueError("y_true and y_prob must have the same length")
    if y_true.size == 0:
        raise ValueError("inputs are empty")
    if not np.all((y_true == 0) | (y_true == 1)):
        raise ValueError("y_true must contain only 0 and 1")
    if np.any((y_prob < 0) | (y_prob > 1)):
        raise ValueError("probabilities must lie in [0, 1]")
    return float(np.mean((y_prob - y_true) ** 2))
