import numpy as np

def solve(X, h0, Wx, Wh, b):
    """Return tanh-RNN hidden states in input sequence order."""
    hidden = np.asarray(h0, dtype=float)
    states = []
    for value in np.asarray(X):
        hidden = np.tanh(np.asarray(Wx) @ value + np.asarray(Wh) @ hidden + b)
        states.append(hidden.copy())
    return np.asarray(states)
