import numpy as np


def paired_t_statistic(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 1 or a.shape != b.shape:
        raise ValueError("a and b must be 1-D with the same length")
    if a.size < 2:
        raise ValueError("need at least two paired scores")
    d = a - b
    sd = d.std(ddof=1)
    if sd == 0:
        raise ValueError("differences have zero spread, so t is undefined")
    return float(d.mean() / (sd / np.sqrt(d.size)))
