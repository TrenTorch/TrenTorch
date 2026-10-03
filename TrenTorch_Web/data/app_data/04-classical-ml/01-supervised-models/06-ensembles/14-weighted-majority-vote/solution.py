import numpy as np


def weighted_majority_vote(predictions: np.ndarray, weights: np.ndarray) -> np.ndarray:
    predictions = np.asarray(predictions, dtype=int)
    weights = np.asarray(weights, dtype=float)
    if predictions.ndim != 2 or len(weights) != predictions.shape[0]:
        raise ValueError("weights must have one entry per classifier row")
    if np.any(weights < 0):
        raise ValueError("weights must be nonnegative")
    if weights.sum() == 0:
        raise ValueError("weights must not all be zero")
    m, n = predictions.shape
    C = predictions.max() + 1
    scores = np.zeros((n, C))
    rows = np.arange(n)
    for j in range(m):
        scores[rows, predictions[j]] += weights[j]
    return np.argmax(scores, axis=1)
