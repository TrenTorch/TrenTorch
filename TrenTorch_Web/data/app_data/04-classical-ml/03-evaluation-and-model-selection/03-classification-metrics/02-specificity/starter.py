import numpy as np


def specificity(y_true: np.ndarray, y_pred: np.ndarray, positive=1) -> float:
    """
    TN / (TN + FP), treating `positive` as the positive class and every
    other label as negative. Returns 0.0 when there are no negatives.
    """
    pass
