import numpy as np


def build_causal_mask(seq_len: int) -> np.ndarray:
    mask = np.zeros((seq_len, seq_len))
    upper_triangle = np.triu(np.ones((seq_len, seq_len)), k=1)
    mask[upper_triangle == 1] = -np.inf
    return mask
