import math


def trust_region_step_size(delta, quad):
    return math.sqrt(2 * delta / quad)
