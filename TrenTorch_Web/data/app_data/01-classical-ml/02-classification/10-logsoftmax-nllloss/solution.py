import numpy as np


def log_softmax(Z: np.ndarray) -> np.ndarray:
    Z_shift = Z - np.max(Z, axis=1, keepdims=True)
    return Z_shift - np.log(np.sum(np.exp(Z_shift), axis=1, keepdims=True))


def nll_loss(log_probs: np.ndarray, y_indices: np.ndarray) -> float:
    n = log_probs.shape[0]
    return float(-np.mean(log_probs[np.arange(n), y_indices]))
