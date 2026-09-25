import numpy as np


def gaussian_pdf(x, mu, sigma):
    """
    x:     scalar or NumPy array of any shape
    mu:    the mean
    sigma: the standard deviation (> 0)

    Returns:
        the Gaussian probability density at x, same shape as x.
    """
    # TODO: Implement the closed-form Gaussian PDF from Theory.
    pass


def sample_gaussian(mu, sigma, n, uniform_draws):
    """
    mu, sigma:     Gaussian parameters
    n:             number of samples to return
    uniform_draws: exactly 2 * n floats in [0, 1), pre-generated

    Returns:
        n Gaussian-distributed samples, as a flat array.
    """
    # TODO: Implement Box-Muller from Theory. Consume uniform_draws in
    # pairs (u1, u2) to produce standard-normal samples in pairs (z0, z1),
    # then shift/scale by mu and sigma. Only slice down to n at the end.
    pass
