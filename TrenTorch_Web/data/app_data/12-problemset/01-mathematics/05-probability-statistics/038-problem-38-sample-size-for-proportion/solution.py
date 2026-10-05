import numpy as np

def solve(p1, p2):
    z_alpha, z_power = 1.96, 0.84
    pooled = (p1 + p2) / 2
    numerator = 2 * (z_alpha * np.sqrt(2 * pooled * (1 - pooled)) + z_power * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return int(np.ceil(numerator / (p1 - p2) ** 2))
