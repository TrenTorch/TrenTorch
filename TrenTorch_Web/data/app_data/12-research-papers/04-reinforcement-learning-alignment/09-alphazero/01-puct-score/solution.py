import math


def puct_score(Q, P, N_parent, N_child, c):
    return Q + c * P * math.sqrt(N_parent) / (1 + N_child)
