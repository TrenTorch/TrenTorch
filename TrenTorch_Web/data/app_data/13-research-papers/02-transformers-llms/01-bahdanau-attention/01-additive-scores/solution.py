import numpy as np


def additive_scores(s, H, W, U, v):
    return np.tanh(s @ W.T + H @ U.T) @ v
