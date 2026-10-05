import math


def permutations_count(n, k):
    return math.factorial(n) // math.factorial(n - k)


def combinations_count(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
