import numpy as np


def cohens_kappa(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    (p_o - p_e) / (1 - p_e) for two labelings of the same items.
    Returns 1.0 when p_e is 1. Raises ValueError on length mismatch or empty input.
    """
    pass
