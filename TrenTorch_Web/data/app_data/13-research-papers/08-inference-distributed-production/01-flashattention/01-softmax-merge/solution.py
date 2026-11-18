import math


def online_softmax_merge(m1, l1, m2, l2):
    m = max(m1, m2)
    l = l1 * math.exp(m1 - m) + l2 * math.exp(m2 - m)
    return m, l
