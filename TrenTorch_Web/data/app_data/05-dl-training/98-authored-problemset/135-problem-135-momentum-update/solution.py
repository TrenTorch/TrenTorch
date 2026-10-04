import numpy as np

def solve(w, v, grad, lr, mu):
    """Implement momentum update according to the contract."""
    v = mu * np.asarray(v) + np.asarray(grad)
    return (v, np.asarray(w) - lr * v)
