import numpy as np

def solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08, wd=0.01):
    """Implement adamw decoupled decay according to the contract."""
    w, g, m, v = map(lambda x: np.asarray(x, float), (w, g, m, v))
    m = beta1 * m + (1 - beta1) * g
    v = beta2 * v + (1 - beta2) * g * g
    mh = m / (1 - beta1 ** t)
    vh = v / (1 - beta2 ** t)
    return (w - lr * (mh / (np.sqrt(vh) + eps) + wd * w), m, v)
