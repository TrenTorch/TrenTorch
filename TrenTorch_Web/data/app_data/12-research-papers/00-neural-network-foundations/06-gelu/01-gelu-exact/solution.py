import math

import numpy as np


def gelu_exact(x):
    x = np.asarray(x, dtype=float)
    phi = np.vectorize(lambda v: 0.5 * (1.0 + math.erf(v / math.sqrt(2.0))))
    return x * phi(x)
