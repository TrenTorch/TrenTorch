import numpy as np


def mgf(values, probabilities, t):
    """
    values: 1D array-like of the outcomes X can take
    probabilities: 1D array-like, same length, non-negative, sums to 1
    t: float or NumPy array

    Returns:
        The moment generating function E[exp(t * X)] at t, with the same
        shape as t.
    """
    # TODO: Implement the weighted sum from Theory.
    pass


def pgf(probabilities, z):
    """
    probabilities: 1D array-like where probabilities[k] = P(X = k)
    z: float or NumPy array

    Returns:
        The probability generating function E[z ** X] at z, with the same
        shape as z.
    """
    # TODO: Implement the series from Theory with the probabilities as
    # coefficients.
    pass


def mgf_moments(mgf_fn, step=1e-3):
    """
    mgf_fn: function taking a float t and returning a float M(t)
    step: the finite-difference step h

    Returns:
        (first_moment, second_moment) as floats: M'(0) and M''(0),
        estimated with central finite differences of size `step`.
    """
    # TODO: Differentiate numerically at t = 0, as in Theory.
    pass


def pgf_mean_variance(probabilities):
    """
    probabilities: 1D array-like where probabilities[k] = P(X = k)

    Returns:
        (mean, variance) as floats, computed from the derivatives of the
        probability generating function at z = 1.
    """
    # TODO: Use G'(1), G''(1) and the variance identity from Theory.
    pass


def sum_distribution(p, q):
    """
    p, q: probability lists for independent X and Y, where p[k] = P(X = k)
        and q[k] = P(Y = k)

    Returns:
        A 1D array of length len(p) + len(q) - 1 holding P(X + Y = n).
    """
    # TODO: Multiply the two generating functions, as in Theory.
    pass
