import numpy as np


def disagreement(correct_a: np.ndarray, correct_b: np.ndarray) -> float:
    a = np.asarray(correct_a).astype(bool)
    b = np.asarray(correct_b).astype(bool)
    if a.ndim != 1 or a.shape != b.shape or len(a) == 0:
        raise ValueError("inputs must be non-empty 1-D arrays of the same length")
    return float(np.count_nonzero(a != b) / len(a))
