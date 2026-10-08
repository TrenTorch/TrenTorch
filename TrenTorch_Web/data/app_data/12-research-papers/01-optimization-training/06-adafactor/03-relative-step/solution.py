import math


def relative_step(t):
    return min(1e-2, 1.0 / math.sqrt(t))
