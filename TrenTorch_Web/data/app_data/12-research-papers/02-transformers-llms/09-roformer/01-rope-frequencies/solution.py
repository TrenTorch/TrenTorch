import numpy as np


def rope_frequencies(d, base=10000.0):
    return base ** (-2.0 * np.arange(d // 2) / d)
