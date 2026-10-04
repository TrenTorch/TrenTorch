import numpy as np

def solve(x, norm, attention, ff):
    """Implement pre-norm transformer block according to the contract."""
    y = norm(x)
    return x + attention(y) + ff(y)
