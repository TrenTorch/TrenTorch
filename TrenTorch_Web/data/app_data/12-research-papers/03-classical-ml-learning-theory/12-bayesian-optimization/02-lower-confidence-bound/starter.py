import numpy as np


def lower_confidence_bound(mu, sigma, kappa):
    """
    mu: predicted mean of the objective (minimization), shape (n,)
    sigma: predicted standard deviation, shape (n,)
    kappa: how strongly to favor uncertain points, non-negative

    Returns:
        mu - kappa * sigma for each candidate. Lower values are more promising.
    """
    # TODO: Subtract kappa times the uncertainty from the predicted mean (see Theory).
    pass
