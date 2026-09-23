import numpy as np

_EPS = 1e-12


def cross_entropy(p: np.ndarray, q: np.ndarray, base: float = 2.0) -> float:
    clipped_q = np.clip(q, _EPS, 1.0)
    return float(-np.sum(p * np.log(clipped_q)) / np.log(base))
