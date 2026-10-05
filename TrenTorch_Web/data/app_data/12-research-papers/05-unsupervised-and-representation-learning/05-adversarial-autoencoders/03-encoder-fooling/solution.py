import numpy as np


def encoder_fooling_loss(d_codes):
    d_codes = np.asarray(d_codes, dtype=float)
    return float(-np.mean(np.log(d_codes)))
