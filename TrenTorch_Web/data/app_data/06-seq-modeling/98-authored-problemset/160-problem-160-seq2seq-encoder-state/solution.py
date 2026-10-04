import numpy as np

def solve(X, h0, Wx, Wh, b):
    """Implement seq2seq encoder state according to the contract."""
    h = np.asarray(h0, float)
    X, Wx, Wh, b = map(np.asarray, (X, Wx, Wh, b))
    for x in X:
        h = np.tanh(Wx @ x + Wh @ h + b)
    return h
