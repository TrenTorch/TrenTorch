import numpy as np

def solve(logits, temperature):
    """Implement softmax temperature according to the contract."""
    z = np.asarray(logits, float) / temperature
    z -= z.max()
    p = np.exp(z)
    return p / p.sum()
