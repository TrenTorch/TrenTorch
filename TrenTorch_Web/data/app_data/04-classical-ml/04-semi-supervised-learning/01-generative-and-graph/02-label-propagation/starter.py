import numpy as np


def propagate(W: np.ndarray, Y0: np.ndarray, alpha: float, iters: int) -> np.ndarray:
    """
    Label propagation F <- alpha * S F + (1 - alpha) * Y0 with
    S = D^(-1/2) W D^(-1/2), starting from F = Y0, for `iters` iterations.
    Raise ValueError for a non-symmetric or negative W, a zero-degree node,
    alpha outside (0, 1), a negative iteration count, or a shape mismatch.
    """
    pass
