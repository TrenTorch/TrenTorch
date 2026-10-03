import numpy as np


def standard_scale_no_leakage(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Scale both matrices with the per-column mean and standard deviation
    of X_train only. Columns with zero training standard deviation use
    1.0 instead, so they become zeros. Returns (scaled_train, scaled_test).
    """
    pass
