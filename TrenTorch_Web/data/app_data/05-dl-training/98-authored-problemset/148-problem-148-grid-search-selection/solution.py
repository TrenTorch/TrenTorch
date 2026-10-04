import numpy as np

def solve(results):
    """Implement grid search selection according to the contract."""
    best = min(results, key=lambda r: (r['val_loss'], str(r['params'])))
    return best
