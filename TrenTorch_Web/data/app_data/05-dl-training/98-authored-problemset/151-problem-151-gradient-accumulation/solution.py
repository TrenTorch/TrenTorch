import numpy as np

def solve(grads):
    """Implement gradient accumulation according to the contract."""
    return sum((np.asarray(g) for g in grads), np.zeros_like(grads[0])) / len(grads)
