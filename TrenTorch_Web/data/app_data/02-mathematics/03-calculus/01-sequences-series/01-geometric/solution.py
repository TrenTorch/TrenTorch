import math


def geometric_partial_sum(a, r, n):
    if r == 1:
        return float(n * a)
    return float(a * (1 - r**n) / (1 - r))


def geometric_series_sum(a, r):
    if abs(r) >= 1:
        raise ValueError("a geometric series only has a finite sum when |r| < 1")
    return float(a / (1 - r))


def terms_needed(a, r, tolerance):
    if abs(r) >= 1:
        raise ValueError("a geometric series only has a finite sum when |r| < 1")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if a == 0:
        return 0

    def gap(n):
        return abs(a * r**n / (1 - r))

    if gap(0) < tolerance:
        return 0
    if r == 0:
        return 1
    n = max(0, math.ceil(math.log(tolerance * abs(1 - r) / abs(a)) / math.log(abs(r))))
    while n > 0 and gap(n - 1) < tolerance:
        n -= 1
    while gap(n) >= tolerance:
        n += 1
    return n
