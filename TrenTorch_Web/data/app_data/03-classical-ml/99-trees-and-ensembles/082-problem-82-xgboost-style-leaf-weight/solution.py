import numpy as np

def solve(G, H, lam):
    """Implement xgboost-style leaf weight according to the contract."""
    return -G / (H + lam)
