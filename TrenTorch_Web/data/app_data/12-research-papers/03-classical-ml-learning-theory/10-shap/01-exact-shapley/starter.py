import math
from itertools import permutations

import numpy as np


def shapley_exact(f, x, baseline):
    """
    f: model, a function taking a feature vector and returning a float
    x: the input to explain, shape (n,)
    baseline: reference input, shape (n,), used for features not yet "revealed"

    Returns:
        The exact Shapley value of each feature, shape (n,), averaged over all orderings.
    """
    # TODO: For every ordering of features, add each feature's marginal contribution, then average (see Theory).
    pass
