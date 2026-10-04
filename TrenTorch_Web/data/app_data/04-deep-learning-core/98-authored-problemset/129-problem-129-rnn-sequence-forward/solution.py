import numpy as np

def solve(X, h0, Wx, Wh, b):
    """Implement rnn sequence forward according to the contract."""
    h = np.asarray(h0, float)
    X, Wx, Wh, b = map(np.asarray, (X, Wx, Wh, b))
    states = []
    for x in X:
        h = np.tanh(Wx @ x + Wh @ h + b)
        states.append(h.copy())
    return np.asarray(states)
