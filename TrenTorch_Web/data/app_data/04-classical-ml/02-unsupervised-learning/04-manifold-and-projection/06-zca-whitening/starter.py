import numpy as np


def zca_whiten(X: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """
    ZCA whitening of X (centered, then decorrelated and rescaled to unit
    variance while staying as close to the original axes as possible).
    Raises ValueError for fewer than 2 rows or negative eps.
    """
    pass
