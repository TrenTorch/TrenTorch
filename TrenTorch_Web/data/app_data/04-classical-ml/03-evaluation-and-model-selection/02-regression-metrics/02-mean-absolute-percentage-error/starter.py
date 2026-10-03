import numpy as np


def mean_absolute_percentage_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    100 * mean(|y_true - y_pred| / |y_true|). Raises ValueError when the
    shapes differ or when any y_true value is zero.
    """
    pass
