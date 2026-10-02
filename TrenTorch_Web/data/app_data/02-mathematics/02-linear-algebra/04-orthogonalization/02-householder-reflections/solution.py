import numpy as np


def householder_vector(x):
    x = np.asarray(x, dtype=float)
    norm = np.linalg.norm(x)
    v = x.copy()
    if norm == 0.0:
        return v
    sign = 1.0 if x[0] >= 0 else -1.0
    v[0] += sign * norm
    return v


def householder_matrix(v):
    v = np.asarray(v, dtype=float)
    n = len(v)
    denominator = v @ v
    if denominator == 0.0:
        return np.eye(n)
    return np.eye(n) - 2.0 * np.outer(v, v) / denominator


def apply_householder(v, a):
    v = np.asarray(v, dtype=float)
    a = np.asarray(a, dtype=float)
    denominator = v @ v
    if denominator == 0.0:
        return a.copy()
    projection = v @ a
    if a.ndim == 1:
        return a - 2.0 * projection * v / denominator
    return a - 2.0 * np.outer(v, projection) / denominator
