import numpy as np

def solve(p1, p2):
    if not (0 <= p1 <= 1 and 0 <= p2 <= 1):
        raise ValueError("p1 and p2 must be probabilities in [0, 1]")
    if p1 == p2:
        raise ValueError("p1 and p2 must differ")
    z_alpha, z_power = 1.96, 0.84
    pooled = (p1 + p2) / 2
    numerator = (z_alpha * np.sqrt(2 * pooled * (1 - pooled)) + z_power * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return int(np.ceil(numerator / (p1 - p2) ** 2))
