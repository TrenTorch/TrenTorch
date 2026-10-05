import math


def probability_of_improvement(mu, sigma, best):
    """
    mu: predicted mean of the objective at a candidate point (minimization)
    sigma: predicted standard deviation at that point, positive
    best: best (lowest) objective value observed so far

    Returns:
        The probability that the candidate's true value beats best, as a float.
    """
    # TODO: Return the standard normal CDF of z = (best - mu) / sigma (see Theory).
    pass
