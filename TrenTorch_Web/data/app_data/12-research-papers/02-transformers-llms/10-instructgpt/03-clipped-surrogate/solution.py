import numpy as np


def clipped_surrogate(ratio, advantage, eps=0.2):
    ratio = np.asarray(ratio, dtype=float)
    advantage = np.asarray(advantage, dtype=float)
    clipped = np.clip(ratio, 1 - eps, 1 + eps)
    return np.minimum(ratio * advantage, clipped * advantage)
