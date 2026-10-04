import numpy as np

def solve(beams, alpha):
    """Implement length-normalized beam search according to the contract."""
    return max(beams, key=lambda z: z[1] / len(z[0]) ** alpha)
