import math


def mi_lower_bound(n_candidates, loss):
    return math.log(n_candidates) - loss
