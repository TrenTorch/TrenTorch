import numpy as np


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    1 - SS_res / SS_tot. Raises ValueError when the shapes differ or
    when y_true is constant (SS_tot is zero, so the score is undefined).
    """
    pass
