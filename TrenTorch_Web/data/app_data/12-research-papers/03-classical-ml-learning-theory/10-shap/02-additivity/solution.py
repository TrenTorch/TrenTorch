import numpy as np


def additivity_gap(phi, f_x, f_base):
    return float(np.sum(phi) - (f_x - f_base))
