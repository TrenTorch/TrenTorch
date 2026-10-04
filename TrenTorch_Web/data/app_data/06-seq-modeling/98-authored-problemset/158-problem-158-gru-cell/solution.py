import numpy as np

def solve(x, h, W, b, Wh, bh):
    """Implement gru cell according to the contract."""
    x, h, W, b, Wh, bh = map(lambda v: np.asarray(v, float), (x, h, W, b, Wh, bh))
    z = W @ np.r_[x, h] + b
    r, u = np.split(z, 2)
    r = 1 / (1 + np.exp(-r))
    u = 1 / (1 + np.exp(-u))
    htilde = np.tanh(Wh @ np.r_[x, r * h] + bh)
    return (1 - u) * h + u * htilde
