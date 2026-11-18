import math

import numpy as np


def gelu_derivative(x):
    x = np.asarray(x, dtype=float)
    cdf = np.vectorize(lambda v: 0.5 * (1.0 + math.erf(v / math.sqrt(2.0))))(x)
    pdf = np.exp(-0.5 * x**2) / math.sqrt(2.0 * math.pi)
    return cdf + x * pdf
