import numpy as np


def expectation(values, probabilities):
    """
    values: 1D array-like, the outcomes a discrete random variable X can take
    probabilities: 1D array-like, P(X = values[i]) for each i

    Returns:
        E[X], as a float, from Theory.
    """
    # TODO: Implement E[X] = sum(x_i * P(x_i)) from Theory.
    pass


def variance(values, probabilities):
    """
    values, probabilities: same as `expectation`

    Returns:
        Var(X) = E[(X - E[X])^2], as a float, from Theory.
    """
    # TODO: Implement Var(X) using `expectation`, from Theory.
    pass


def covariance(x_values, y_values, joint_probabilities):
    """
    x_values: 1D array-like, the outcomes X can take
    y_values: 1D array-like, the outcomes Y can take
    joint_probabilities: 2D array-like, joint_probabilities[i, j] =
        P(X=x_values[i], Y=y_values[j])

    Returns:
        Cov(X, Y) = E[(X - E[X])(Y - E[Y])], as a float, from Theory.
    """
    # TODO: Implement Cov(X, Y) from Theory, using the joint distribution's
    # own marginals for E[X] and E[Y].
    pass
