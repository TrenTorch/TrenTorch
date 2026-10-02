def telescoping_partial_sum(f, n):
    if n == 0:
        return 0.0
    return float(f(1) - f(n + 1))


def telescoping_infinite_sum(f_first, f_limit):
    return float(f_first - f_limit)


def sum_reciprocal_products(n):
    return n / (n + 1)
