import numpy as np


def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))


def mean_pass_at_k(ns, cs, k):
    return float(np.mean([pass_at_k(n, c, k) for n, c in zip(ns, cs)]))
