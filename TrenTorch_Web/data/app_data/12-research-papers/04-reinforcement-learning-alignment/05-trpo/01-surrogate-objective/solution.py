import numpy as np


def surrogate_objective(ratio, advantage):
    return float(np.mean(np.asarray(ratio, dtype=float) * np.asarray(advantage, dtype=float)))
