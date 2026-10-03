import numpy as np


def matthews_corrcoef(y_true: np.ndarray, y_pred: np.ndarray, positive=1) -> float:
    """
    Matthews correlation coefficient for binary labels, with `positive` as
    the positive class. Returns 0.0 when any marginal total is zero.
    Raises ValueError on length mismatch.
    """
    pass
