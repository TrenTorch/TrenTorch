import numpy as np


def discriminator_score(local, global_vec, W):
    return float(np.asarray(local, dtype=float) @ np.asarray(W, dtype=float) @ np.asarray(global_vec, dtype=float))
