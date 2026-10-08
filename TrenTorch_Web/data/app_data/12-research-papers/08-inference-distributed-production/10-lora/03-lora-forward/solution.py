import numpy as np


def lora_forward(x, W, A, B, scale):
    return np.asarray(x, dtype=float) @ np.asarray(W, dtype=float).T + scale * (
        np.asarray(x, dtype=float) @ np.asarray(A, dtype=float).T
    ) @ np.asarray(B, dtype=float).T
