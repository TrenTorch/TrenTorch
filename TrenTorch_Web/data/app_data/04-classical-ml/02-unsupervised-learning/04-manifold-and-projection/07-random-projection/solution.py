import numpy as np


def gaussian_random_projection(X: np.ndarray, k: int, seed: int = 0) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if k < 1:
        raise ValueError("k must be at least 1")
    rng = np.random.default_rng(seed)
    R = rng.normal(size=(X.shape[1], k)) / np.sqrt(k)
    return X @ R
