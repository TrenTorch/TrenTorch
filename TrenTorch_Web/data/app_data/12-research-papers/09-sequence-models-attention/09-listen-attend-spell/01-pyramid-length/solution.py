import math


def pyramid_length(T, layers):
    return math.ceil(T / 2**layers)
