import numpy as np


def reparameterize(mu, logvar, eps):
    """
    mu: mean of the approximate posterior q(z | x)
    logvar: log of its variance
    eps: a standard normal draw with the same shape

    Returns:
        A sample z = mu + exp(0.5 * logvar) * eps that is differentiable in mu and logvar.
    """
    # TODO: Scale the noise by the standard deviation and shift by the mean (see Theory).
    pass
