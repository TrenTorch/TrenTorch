import math


def subsample_keep_prob(freq, t):
    return min(1.0, math.sqrt(t / freq))
