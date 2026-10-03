import numpy as np


def f1_micro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    F1 from counts pooled over all classes: 2TP / (2TP + FP + FN).
    Raises ValueError on length mismatch or empty input.
    """
    pass


def f1_macro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Mean of per-class F1 over the union of labels. A class whose F1
    denominator is zero contributes 0.0.
    """
    pass
