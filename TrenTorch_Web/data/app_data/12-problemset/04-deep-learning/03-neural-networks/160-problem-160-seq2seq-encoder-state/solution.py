import numpy as np

def solve(X, h0, Wx, Wh, b):
    """Return the final hidden state after encoding X with a tanh RNN."""
    hidden = np.asarray(h0, dtype=float)
    for value in np.asarray(X):
        hidden = np.tanh(np.asarray(Wx) @ value + np.asarray(Wh) @ hidden + b)
    return hidden
