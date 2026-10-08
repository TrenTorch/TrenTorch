import math


def perplexity(total_nll, n):
    return math.exp(total_nll / n)
