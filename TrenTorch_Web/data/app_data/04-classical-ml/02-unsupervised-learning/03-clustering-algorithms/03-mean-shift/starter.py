import numpy as np


def mean_shift(X: np.ndarray, bandwidth: float, max_iter: int = 300, tol: float = 1e-6) -> np.ndarray:
    """
    Gaussian-kernel mean shift. Returns integer labels, one per row of X.
    Modes closer than bandwidth / 2 are merged. Raises ValueError when
    bandwidth is not positive.
    """
    pass
