import math


def triangular_lr(it, base, max_lr, step):
    cycle = math.floor(1 + it / (2 * step))
    x = abs(it / step - 2 * cycle + 1)
    return base + (max_lr - base) * max(0.0, 1 - x)
