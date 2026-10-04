import numpy as np

def solve(coeffs):
    """Implement solve a 2×2 linear system according to the contract."""
    a, b, c, d, e, f = coeffs
    det = a * d - b * c
    if det == 0:
        raise ValueError('singular system')
    return np.array([(e * d - b * f) / det, (a * f - e * c) / det])
