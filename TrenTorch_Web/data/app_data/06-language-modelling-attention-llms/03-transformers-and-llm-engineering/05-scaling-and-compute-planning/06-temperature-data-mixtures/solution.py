import numpy as np


def mixture_weights(sizes, temperature):
    s = np.asarray(sizes, dtype=float) ** (1.0 / temperature)
    return s / s.sum()


def epochs_per_source(sizes, weights, total_tokens):
    return np.asarray(weights, dtype=float) * total_tokens / np.asarray(sizes, dtype=float)
