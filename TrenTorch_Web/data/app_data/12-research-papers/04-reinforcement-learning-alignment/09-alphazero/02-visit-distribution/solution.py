import numpy as np


def visit_distribution(counts, tau):
    counts = np.asarray(counts, dtype=float)
    powered = counts ** (1.0 / tau)
    return powered / powered.sum()
