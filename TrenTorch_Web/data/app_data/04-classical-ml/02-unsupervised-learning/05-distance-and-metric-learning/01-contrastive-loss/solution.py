import numpy as np


def contrastive_loss(distances: np.ndarray, is_similar: np.ndarray, margin: float = 1.0) -> np.ndarray:
    d = np.asarray(distances, dtype=float)
    s = np.asarray(is_similar, dtype=float)
    if d.shape != s.shape:
        raise ValueError("distances and is_similar must have the same shape")
    if np.any(d < 0):
        raise ValueError("distances must be nonnegative")
    if margin < 0:
        raise ValueError("margin must be nonnegative")
    if not np.all(np.isin(s, [0.0, 1.0])):
        raise ValueError("is_similar must hold 0 or 1")
    return s * d ** 2 + (1.0 - s) * np.maximum(0.0, margin - d) ** 2
