import numpy as np

def solve(in_features, out_features, r):
    """Implement lora parameter count according to the contract."""
    return r * (in_features + out_features)
