import numpy as np


def gru_step(x, h, Wz, Uz, Wr, Ur, W, U):
    z = 1.0 / (1.0 + np.exp(-(Wz @ x + Uz @ h)))
    r = 1.0 / (1.0 + np.exp(-(Wr @ x + Ur @ h)))
    h_tilde = np.tanh(W @ x + U @ (r * h))
    return (1 - z) * h + z * h_tilde
