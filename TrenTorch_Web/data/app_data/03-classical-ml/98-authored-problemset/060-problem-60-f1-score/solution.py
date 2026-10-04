import numpy as np

def solve(precision, recall):
    """Implement f1 score according to the contract."""
    p, r = (precision, recall)
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)
