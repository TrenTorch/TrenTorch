import numpy as np


def smoothed_probabilities(counts, alpha=1.0):
    smoothed = np.asarray(counts, dtype=float) + alpha
    return smoothed / smoothed.sum(axis=1, keepdims=True)
