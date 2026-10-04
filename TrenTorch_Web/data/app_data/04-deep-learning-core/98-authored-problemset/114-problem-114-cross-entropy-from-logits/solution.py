import numpy as np

def solve(logits, target):
    """Implement cross-entropy from logits according to the contract."""
    z = np.asarray(logits, float)
    z -= z.max(axis=-1, keepdims=True)
    lp = z - np.log(np.exp(z).sum(axis=-1, keepdims=True))
    target = np.asarray(target)
    if target.ndim == z.ndim - 1:
        return float(-np.mean(np.take_along_axis(lp, target[..., None], axis=-1)))
    return float(-np.mean(np.sum(target * lp, axis=-1)))
