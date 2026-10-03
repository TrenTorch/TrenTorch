import numpy as np


def paired_t_statistic(a: np.ndarray, b: np.ndarray) -> float:
    """
    t = mean(d) / (sd(d) / sqrt(n)) for d = a - b, with sd using n - 1.
    Raise ValueError for mismatched lengths, n < 2, or zero spread in d.
    """
    pass
