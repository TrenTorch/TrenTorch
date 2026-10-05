import numpy as np


def finalize_output(acc, l):
    return np.asarray(acc, dtype=float) / np.asarray(l, dtype=float)[..., None]
