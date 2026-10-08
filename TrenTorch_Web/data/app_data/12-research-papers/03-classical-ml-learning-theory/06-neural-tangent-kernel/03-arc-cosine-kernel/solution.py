import math

import numpy as np


def arc_cosine_kernel(x, y):
    nx = np.linalg.norm(x)
    ny = np.linalg.norm(y)
    if nx * ny == 0:
        return 0.0
    c = np.clip(np.dot(x, y) / (nx * ny), -1.0, 1.0)
    th = math.acos(c)
    return float(nx * ny / (2 * math.pi) * (math.sin(th) + (math.pi - th) * c))
