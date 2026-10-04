import numpy as np


def steering_vector(pos_acts, neg_acts, normalize=True):
    v = np.asarray(pos_acts, float).mean(axis=0) - np.asarray(neg_acts, float).mean(axis=0)
    if normalize:
        norm = np.linalg.norm(v)
        if norm > 0:
            v = v / norm
    return v


def apply_steering(resid, v, alpha, positions=None):
    out = np.array(resid, dtype=float, copy=True)
    if positions is None:
        out += alpha * v
    else:
        out[list(positions)] += alpha * v
    return out
