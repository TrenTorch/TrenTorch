from math import gcd


def euler_phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
