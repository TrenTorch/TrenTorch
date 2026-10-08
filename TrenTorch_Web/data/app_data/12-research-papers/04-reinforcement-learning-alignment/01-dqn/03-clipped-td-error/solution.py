import numpy as np


def clipped_td_error(td, c):
    return np.clip(np.asarray(td, dtype=float), -c, c)
