import numpy as np


def auc_rank(scores: np.ndarray, labels: np.ndarray) -> float:
    """
    ROC AUC via the Mann-Whitney rank statistic with tied ranks averaged.
    Raise ValueError for mismatched lengths, labels outside {0, 1}, or a missing class.
    """
    pass
