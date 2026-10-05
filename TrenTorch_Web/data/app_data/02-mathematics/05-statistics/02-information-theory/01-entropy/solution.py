import numpy as np

_EPS = 1e-12


def entropy(probs: np.ndarray, base: float = 2.0) -> float:
    clipped = np.clip(probs, _EPS, 1.0)
    return float(-np.sum(probs * np.log(clipped)) / np.log(base))
