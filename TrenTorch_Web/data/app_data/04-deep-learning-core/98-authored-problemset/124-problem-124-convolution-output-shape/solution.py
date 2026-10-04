import numpy as np

def solve(W, K, P, S):
    """Implement convolution output shape according to the contract."""
    return (W + 2 * P - K) // S + 1
