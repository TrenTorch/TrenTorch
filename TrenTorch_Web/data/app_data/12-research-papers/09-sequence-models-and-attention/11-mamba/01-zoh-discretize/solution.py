import math


def zoh_discretize(A, B, delta):
    A_bar = math.exp(delta * A)
    B_bar = (A_bar - 1) / A * B
    return A_bar, B_bar
