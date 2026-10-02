import math


def binomial_pmf(n, p, k):
    coefficient = math.comb(n, k)
    return coefficient * (p**k) * ((1 - p) ** (n - k))


def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0
