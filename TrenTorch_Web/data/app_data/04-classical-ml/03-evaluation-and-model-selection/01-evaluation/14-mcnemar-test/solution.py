import numpy as np


def mcnemar_statistic(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> float:
    a_correct = np.asarray(pred_a) == np.asarray(y_true)
    b_correct = np.asarray(pred_b) == np.asarray(y_true)
    only_a = int(np.sum(a_correct & ~b_correct))
    only_b = int(np.sum(~a_correct & b_correct))
    total = only_a + only_b
    if total == 0:
        return 0.0
    return float(max(abs(only_a - only_b) - 1, 0) ** 2 / total)
