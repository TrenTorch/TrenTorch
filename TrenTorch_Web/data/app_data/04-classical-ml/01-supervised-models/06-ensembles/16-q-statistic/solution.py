import numpy as np


def q_statistic(correct_a: np.ndarray, correct_b: np.ndarray) -> float:
    a = np.asarray(correct_a).astype(bool)
    b = np.asarray(correct_b).astype(bool)
    if a.ndim != 1 or a.shape != b.shape or len(a) == 0:
        raise ValueError("inputs must be non-empty 1-D arrays of the same length")
    n11 = float(np.count_nonzero(a & b))
    n10 = float(np.count_nonzero(a & ~b))
    n01 = float(np.count_nonzero(~a & b))
    n00 = float(np.count_nonzero(~a & ~b))
    denom = n11 * n00 + n01 * n10
    if denom == 0:
        raise ValueError("Q is undefined when N11*N00 + N01*N10 is zero")
    return float((n11 * n00 - n01 * n10) / denom)
