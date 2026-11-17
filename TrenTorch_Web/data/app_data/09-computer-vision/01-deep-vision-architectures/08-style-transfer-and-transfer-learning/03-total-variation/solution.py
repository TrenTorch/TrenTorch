import numpy as np


def total_variation(img):
    x = np.asarray(img, dtype=float)
    dv = np.abs(x[..., 1:, :] - x[..., :-1, :]).mean()
    dh = np.abs(x[..., :, 1:] - x[..., :, :-1]).mean()
    return float(0.5 * (dv + dh))
