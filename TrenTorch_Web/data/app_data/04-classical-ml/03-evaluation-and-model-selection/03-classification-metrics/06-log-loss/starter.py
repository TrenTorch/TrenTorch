import numpy as np


def log_loss(y_true: np.ndarray, y_prob: np.ndarray, eps: float = 1e-15) -> float:
    """
    Binary cross-entropy of predicted probabilities for class 1.
    Probabilities are clipped to [eps, 1 - eps]. Raises ValueError on
    bad labels, probabilities outside [0, 1], or mismatched lengths.
    """
    pass
