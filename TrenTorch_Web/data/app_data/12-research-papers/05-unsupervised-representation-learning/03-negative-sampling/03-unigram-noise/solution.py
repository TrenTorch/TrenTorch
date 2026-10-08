import numpy as np


def unigram_noise(counts, power=0.75):
    c = np.asarray(counts, dtype=float) ** power
    return c / c.sum()
