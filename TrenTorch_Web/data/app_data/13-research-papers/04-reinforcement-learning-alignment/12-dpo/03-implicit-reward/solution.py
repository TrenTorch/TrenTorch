import numpy as np


def implicit_reward(logp, ref, beta):
    return beta * (np.asarray(logp, dtype=float) - np.asarray(ref, dtype=float))
