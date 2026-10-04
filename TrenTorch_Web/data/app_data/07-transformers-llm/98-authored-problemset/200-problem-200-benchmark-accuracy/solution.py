import numpy as np

def solve(predictions, targets):
    """Implement benchmark accuracy according to the contract."""
    return float(np.mean([a.strip() == b.strip() for a, b in zip(predictions, targets)]))
