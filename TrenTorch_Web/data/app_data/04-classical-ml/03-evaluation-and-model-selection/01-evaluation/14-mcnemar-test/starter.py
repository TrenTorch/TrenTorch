import numpy as np


def mcnemar_statistic(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> float:
    """
    y_true, pred_a, pred_b: 1-D arrays of equal length.

    Returns:
        the continuity-corrected McNemar chi-square statistic, or 0.0
        if the classifiers never disagree on correctness.
    """
    # TODO: Count the two kinds of disagreement and apply the formula.
    pass
