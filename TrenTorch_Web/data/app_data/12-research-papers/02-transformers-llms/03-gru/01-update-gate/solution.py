import numpy as np


def gru_update_gate(x, h, Wz, Uz):
    return 1.0 / (1.0 + np.exp(-(Wz @ x + Uz @ h)))
