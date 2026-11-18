import numpy as np


def stack_residuals(x, fs):
    out = np.asarray(x, dtype=float)
    for f in fs:
        out = out + f(out)
    return out
