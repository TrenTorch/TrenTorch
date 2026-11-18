import math


def optimal_params_for_budget(flops):
    return math.sqrt(flops / 120.0)
