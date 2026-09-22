import numpy as np


def accuracy(p: np.ndarray, y: np.ndarray) -> float:
    """
    Classification accuracy.

    p, y: shape (n,), each 0 or 1.

    Return (TP + TN) / n: the fraction of rows where p equals y.
    """
    # TODO: (p == y) is a boolean array of exactly the correct rows.
    pass
