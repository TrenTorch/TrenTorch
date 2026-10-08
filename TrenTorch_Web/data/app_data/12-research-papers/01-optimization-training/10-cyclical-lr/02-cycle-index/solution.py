import math


def cycle_index(it, step):
    return math.floor(1 + it / (2 * step))
