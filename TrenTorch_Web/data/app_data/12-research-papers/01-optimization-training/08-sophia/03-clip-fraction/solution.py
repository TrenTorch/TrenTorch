import numpy as np


def clip_fraction(ratios):
    return float(np.mean(np.abs(np.asarray(ratios, dtype=float)) >= 1.0))
