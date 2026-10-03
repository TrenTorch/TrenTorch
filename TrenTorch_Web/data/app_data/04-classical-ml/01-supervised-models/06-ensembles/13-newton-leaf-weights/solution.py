import numpy as np


def logistic_grad_hess(y: np.ndarray, raw: np.ndarray):
    y = np.asarray(y, dtype=float)
    raw = np.asarray(raw, dtype=float)
    if not np.all((y == 0) | (y == 1)):
        raise ValueError("y must contain only 0 and 1")
    p = 1.0 / (1.0 + np.exp(-raw))
    return p - y, p * (1.0 - p)


def leaf_weight(G: float, H: float, lam: float) -> float:
    if lam <= 0:
        raise ValueError("lam must be positive")
    return -G / (H + lam)


def split_gain(G_L: float, H_L: float, G_R: float, H_R: float, lam: float, gamma: float) -> float:
    if lam <= 0:
        raise ValueError("lam must be positive")
    G = G_L + G_R
    H = H_L + H_R
    return 0.5 * (G_L ** 2 / (H_L + lam) + G_R ** 2 / (H_R + lam) - G ** 2 / (H + lam)) - gamma
