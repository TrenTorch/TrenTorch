import numpy as np


def act_output(outs, halts):
    weights = list(halts[:-1]) + [1 - sum(halts[:-1])]
    return float(np.sum(np.asarray(weights) * np.asarray(outs, dtype=float)))
