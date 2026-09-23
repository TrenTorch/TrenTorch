import numpy as np


def softmax(Z: np.ndarray) -> np.ndarray:
    Z_shift = Z - np.max(Z, axis=1, keepdims=True)
    exp_Z = np.exp(Z_shift)
    return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)


def cce_loss(P: np.ndarray, y_indices: np.ndarray) -> float:
    n = P.shape[0]
    p_correct = np.clip(P[np.arange(n), y_indices], 1e-12, 1.0)
    return float(-np.mean(np.log(p_correct)))
