import math


def is_valid_pmf(probabilities):
    return all(p >= 0 for p in probabilities) and abs(sum(probabilities) - 1.0) < 1e-9


def expected_value_discrete(outcomes, probabilities):
    return sum(o * p for o, p in zip(outcomes, probabilities))


def binomial_pmf(n, p, k):
    coefficient = math.comb(n, k)
    return coefficient * (p**k) * ((1 - p) ** (n - k))


def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0
