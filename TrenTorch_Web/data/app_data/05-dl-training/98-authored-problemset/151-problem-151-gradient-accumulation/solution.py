import numpy as np

def solve(grads):
    """Return the elementwise mean of equally shaped micro-batch gradients."""
    if not grads:
        raise ValueError("grads must contain at least one micro-batch")
    arrays = [np.asarray(g, dtype=float) for g in grads]
    if any(g.shape != arrays[0].shape for g in arrays):
        raise ValueError("all gradients must have the same shape")
    return np.mean(np.stack(arrays, axis=0), axis=0)
