import math


def expected_improvement(mu, sigma, best):
    z = (best - mu) / sigma
    Phi = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
    return float((best - mu) * Phi + sigma * phi)
