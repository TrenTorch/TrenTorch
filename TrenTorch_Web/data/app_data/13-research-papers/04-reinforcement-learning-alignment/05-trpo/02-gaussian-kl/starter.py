import math


def gaussian_kl(mu1, s1, mu2, s2):
    """
    mu1, s1: mean and standard deviation of the first Gaussian (s1 > 0)
    mu2, s2: mean and standard deviation of the second Gaussian (s2 > 0)

    Returns:
        KL(N(mu1, s1^2) || N(mu2, s2^2)) as a float.
    """
    # TODO: Apply the closed-form KL between two univariate Gaussians (see Theory).
    pass
