from math import isqrt


def sum_divisor_counts(n):
    r = isqrt(n)
    return 2 * sum(n // j for j in range(1, r + 1)) - r * r
