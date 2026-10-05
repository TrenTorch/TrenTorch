import numpy as np


def prior_sample(rng, n, d):
    return rng.standard_normal((n, d))
