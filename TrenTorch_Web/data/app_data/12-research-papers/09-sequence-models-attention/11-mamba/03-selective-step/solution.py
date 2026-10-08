import numpy as np


def selective_step(delta_raw):
    return float(np.logaddexp(0.0, delta_raw))
