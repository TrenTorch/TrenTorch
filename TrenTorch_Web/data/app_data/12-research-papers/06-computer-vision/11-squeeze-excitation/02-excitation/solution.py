import numpy as np


def excitation(s, W1, W2):
    z = np.maximum(0.0, np.asarray(W1, dtype=float) @ np.asarray(s, dtype=float))
    return 1.0 / (1.0 + np.exp(-(np.asarray(W2, dtype=float) @ z)))
