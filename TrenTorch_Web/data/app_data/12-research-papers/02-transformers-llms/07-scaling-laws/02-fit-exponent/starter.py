import numpy as np


def fit_power_law_exponent(N, L):
    """
    N: model sizes, positive array
    L: measured losses at each size, positive array of the same length

    Returns:
        The exponent alpha of the best-fit power law L = c * N^(-alpha), as a float.
    """
    # TODO: Fit a line to log(L) against log(N) and return the negated slope (see Theory).
    pass
