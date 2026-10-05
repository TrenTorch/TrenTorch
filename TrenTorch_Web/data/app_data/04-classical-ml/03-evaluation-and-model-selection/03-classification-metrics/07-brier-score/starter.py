import numpy as np


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """
    Mean squared difference between predicted probability of class 1 and
    the 0/1 label. Raises ValueError on bad labels, probabilities outside
    [0, 1], or mismatched lengths.
    """
    pass
