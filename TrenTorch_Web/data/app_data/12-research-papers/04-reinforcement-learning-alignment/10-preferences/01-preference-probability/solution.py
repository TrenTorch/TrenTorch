import math


def preference_probability(r_a, r_b):
    return 1.0 / (1.0 + math.exp(-(r_a - r_b)))
