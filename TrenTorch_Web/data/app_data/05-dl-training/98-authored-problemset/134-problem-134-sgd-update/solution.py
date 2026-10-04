import numpy as np

def solve(w, grad, lr):
    """Implement sgd update according to the contract."""
    return np.asarray(w) - lr * np.asarray(grad)
