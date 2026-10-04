import numpy as np

def solve(mean_nll):
    """Implement perplexity from nll according to the contract."""
    return float(np.exp(mean_nll))
