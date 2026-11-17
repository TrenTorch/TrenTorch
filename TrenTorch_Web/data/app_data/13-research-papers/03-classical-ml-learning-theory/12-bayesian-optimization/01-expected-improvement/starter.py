import math


def expected_improvement(mu, sigma, best):
    """
    mu: predicted mean of the objective at a candidate point (minimization)
    sigma: predicted standard deviation at that point, positive
    best: best (lowest) objective value observed so far

    Returns:
        The expected amount by which the candidate improves on best, as a float.
    """
    # TODO: Use the standard normal CDF and density of z = (best - mu) / sigma (see Theory).
    pass
