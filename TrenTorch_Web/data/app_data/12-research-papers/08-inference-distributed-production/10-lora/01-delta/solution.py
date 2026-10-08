import numpy as np


def lora_delta(A, B, alpha, r):
    return (alpha / r) * (np.asarray(B, dtype=float) @ np.asarray(A, dtype=float))
