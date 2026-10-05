import numpy as np


def explained_variance_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    1 - Var(y_true - y_pred) / Var(y_true), with population variance
    (ddof = 0). Raises ValueError when the shapes differ or when y_true
    is constant.
    """
    pass
