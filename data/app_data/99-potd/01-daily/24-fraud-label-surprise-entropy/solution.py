import numpy as np


def entropy(p: np.ndarray) -> float:
    nonzero = p > 0
    contributions = np.zeros_like(p, dtype=float)
    contributions[nonzero] = -p[nonzero] * np.log2(p[nonzero])
    return float(np.sum(contributions))
