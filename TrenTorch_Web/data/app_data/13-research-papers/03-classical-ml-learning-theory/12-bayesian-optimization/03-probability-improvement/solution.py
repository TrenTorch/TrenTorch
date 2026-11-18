import math


def probability_of_improvement(mu, sigma, best):
    z = (best - mu) / sigma
    return float(0.5 * (1.0 + math.erf(z / math.sqrt(2.0))))
