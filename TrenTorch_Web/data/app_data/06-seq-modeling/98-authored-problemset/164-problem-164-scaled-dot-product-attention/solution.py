import numpy as np

def solve(Q, K, V, mask=None):
    """Implement scaled dot-product attention according to the contract."""
    Q, K, V = map(np.asarray, (Q, K, V))
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None:
        scores = np.where(mask, scores, -1000000000.0)
    scores -= scores.max(axis=-1, keepdims=True)
    A = np.exp(scores)
    A /= A.sum(axis=-1, keepdims=True)
    return A @ V
