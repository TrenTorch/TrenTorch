import numpy as np

def solve(x, norm, attention, ff):
    """Implement post-norm transformer block according to the contract."""
    y = norm(x + attention(x))
    return norm(y + ff(y))
