from math import comb


def binomial_mod(n, k):
    if k < 0 or k > n:
        return 0
    return comb(n, k) % (10**9 + 7)
