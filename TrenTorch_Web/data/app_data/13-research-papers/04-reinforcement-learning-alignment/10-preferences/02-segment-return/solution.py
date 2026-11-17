import numpy as np


def segment_return(rewards):
    return float(np.sum(np.asarray(rewards, dtype=float)))
