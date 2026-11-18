from math import isqrt


def num_squares(n):
    if n == 0:
        return 0
    if isqrt(n) ** 2 == n:
        return 1
    m = n
    while m % 4 == 0:
        m //= 4
    if m % 8 == 7:
        return 4
    i = 1
    while i * i <= n:
        rest = n - i * i
        if isqrt(rest) ** 2 == rest:
            return 2
        i += 1
    return 3
