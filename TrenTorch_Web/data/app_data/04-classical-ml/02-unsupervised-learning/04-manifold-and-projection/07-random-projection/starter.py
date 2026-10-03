import numpy as np


def gaussian_random_projection(X: np.ndarray, k: int, seed: int = 0) -> np.ndarray:
    """
    Project rows of X to k dimensions with a Gaussian matrix scaled by
    1/sqrt(k). Deterministic for a given seed. Raises ValueError when k < 1.
    """
    pass
