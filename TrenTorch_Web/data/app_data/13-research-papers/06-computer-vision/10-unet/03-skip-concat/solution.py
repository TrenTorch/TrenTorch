import numpy as np


def skip_concat(enc, dec):
    return np.concatenate([np.asarray(enc, dtype=float), np.asarray(dec, dtype=float)], axis=-1)
