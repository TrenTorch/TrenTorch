import numpy as np


def kl_std_normal(mu, logvar):
    """
    mu: posterior means, one per latent dimension
    logvar: posterior log-variances, same shape

    Returns:
        KL(q(z|x) || N(0, I)) summed over latent dimensions, as a float.
    """
    # TODO: Apply the closed-form Gaussian KL summed over dimensions (see Theory).
    pass
