import numpy as np

def solve(grad, direction):
    direction = np.asarray(direction, dtype=float)
    direction = direction / np.linalg.norm(direction)
    return float(np.asarray(grad, dtype=float) @ direction)
