import numpy as np


def causal_mask(n):
    return np.tril(np.ones((n, n), dtype=bool))
