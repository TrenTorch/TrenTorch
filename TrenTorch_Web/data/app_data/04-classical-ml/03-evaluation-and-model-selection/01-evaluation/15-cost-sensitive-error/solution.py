import numpy as np


def cost_sensitive_error(y_true: np.ndarray, y_pred: np.ndarray, cost_matrix: np.ndarray) -> float:
    y_true = np.asarray(y_true)
    if y_true.size == 0:
        return 0.0
    costs = np.asarray(cost_matrix, dtype=float)[y_true, np.asarray(y_pred)]
    return float(np.mean(costs))
