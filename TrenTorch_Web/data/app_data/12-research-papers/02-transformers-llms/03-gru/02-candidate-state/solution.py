import numpy as np


def gru_candidate(x, h, r, W, U):
    return np.tanh(W @ x + U @ (r * h))
