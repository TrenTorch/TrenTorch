import numpy as np

def solve(x, h, Wx, Wh, b):
    """Implement rnn step according to the contract."""
    x, h, Wx, Wh, b = map(np.asarray, (x, h, Wx, Wh, b))
    return np.tanh(Wx @ x + Wh @ h + b)
