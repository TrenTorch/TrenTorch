import numpy as np

def solve(target, predicted, use_target):
    """Implement teacher forcing step according to the contract."""
    return target if use_target else predicted
