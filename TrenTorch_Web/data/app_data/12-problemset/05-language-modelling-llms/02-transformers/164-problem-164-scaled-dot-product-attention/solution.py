import numpy as np

def solve(Q, K, V, mask=None):
    """Compute scaled dot-product attention; True mask entries are allowed."""
    Q, K, V = (np.asarray(value, dtype=float) for value in (Q, K, V))
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None:
        mask = np.asarray(mask, dtype=bool)
        scores = np.where(mask, scores, -np.inf)
    row_max = np.max(scores, axis=-1, keepdims=True)
    row_max = np.where(np.isfinite(row_max), row_max, 0)
    weights = np.exp(scores - row_max)
    denominator = weights.sum(axis=-1, keepdims=True)
    weights = np.divide(weights, denominator, out=np.zeros_like(weights), where=denominator != 0)
    return weights @ V
