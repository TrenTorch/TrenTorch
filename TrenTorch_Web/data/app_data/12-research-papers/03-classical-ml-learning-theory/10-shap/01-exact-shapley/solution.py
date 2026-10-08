import math
from itertools import permutations

import numpy as np


def shapley_exact(f, x, baseline):
    x = np.asarray(x, dtype=float)
    n = len(x)
    phi = np.zeros(n)
    for perm in permutations(range(n)):
        cur = np.asarray(baseline, dtype=float).copy()
        for i in perm:
            prev = f(cur)
            cur[i] = x[i]
            phi[i] += f(cur) - prev
    return phi / math.factorial(n)
