import math


def reward_model_nll(y, r_a, r_b):
    p = 1.0 / (1.0 + math.exp(-(r_a - r_b)))
    p = min(max(p, 1e-12), 1 - 1e-12)
    return float(-(y * math.log(p) + (1 - y) * math.log(1 - p)))
