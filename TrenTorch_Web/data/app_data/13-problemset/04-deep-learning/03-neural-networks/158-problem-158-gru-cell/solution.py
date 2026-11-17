import numpy as np

def solve(x, h, W, b, Wh, bh):
    """Apply a GRU update using reset and update gates, then return the state."""
    gates = np.asarray(W) @ np.r_[x, h] + b
    reset, update = np.split(gates, 2)
    sigmoid = lambda z: 1 / (1 + np.exp(-z))
    candidate = np.tanh(np.asarray(Wh) @ np.r_[x, sigmoid(reset) * h] + bh)
    return (1 - sigmoid(update)) * h + sigmoid(update) * candidate
