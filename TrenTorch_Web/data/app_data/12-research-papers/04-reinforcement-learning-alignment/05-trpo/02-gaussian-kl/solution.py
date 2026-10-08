import math


def gaussian_kl(mu1, s1, mu2, s2):
    return math.log(s2 / s1) + (s1**2 + (mu1 - mu2) ** 2) / (2 * s2**2) - 0.5
