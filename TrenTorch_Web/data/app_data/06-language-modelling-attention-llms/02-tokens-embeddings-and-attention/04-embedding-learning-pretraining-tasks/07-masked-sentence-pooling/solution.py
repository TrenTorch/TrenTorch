import numpy as np


def pool_sentence(hidden, mask, mode):
    hidden = np.asarray(hidden, dtype=float)
    mask = np.asarray(mask)
    if mode == "cls":
        return hidden[:, 0]
    if mode == "mean":
        return (hidden * mask[..., None]).sum(axis=1) / mask.sum(axis=1, keepdims=True)
    if mode == "max":
        return np.where(mask[..., None] == 1, hidden, -np.inf).max(axis=1)
    raise ValueError(f"unknown mode: {mode}")
