import numpy as np


def hard_vote(predictions: np.ndarray) -> np.ndarray:
    preds = np.asarray(predictions)
    out = np.empty(preds.shape[1], dtype=preds.dtype)
    for j in range(preds.shape[1]):
        values, counts = np.unique(preds[:, j], return_counts=True)
        out[j] = values[np.argmax(counts)]
    return out


def soft_vote(probabilities: np.ndarray, weights=None) -> np.ndarray:
    probs = np.asarray(probabilities, dtype=float)
    w = np.ones(probs.shape[0]) if weights is None else np.asarray(weights, dtype=float)
    mean = np.tensordot(w, probs, axes=(0, 0)) / w.sum()
    return np.argmax(mean, axis=1)
