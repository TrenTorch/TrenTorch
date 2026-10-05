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


def pmf_covariance(x_values, y_values, joint_probabilities):
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


def sample_mean(x: np.ndarray) -> float:
    """
    The sample mean estimates a distribution's expectation E[X]:
    simply the average of the observed values.
    """
    pass


def sample_variance(x: np.ndarray, ddof: int = 0) -> float:
    """
    The sample variance estimates a distribution's Var(X). `ddof`
    ("delta degrees of freedom") controls the divisor: ddof=0 divides
    by n (the biased/population estimator), ddof=1 divides by n-1
    (Bessel's correction, the unbiased estimator). See Theory for why
    the distinction matters.
    """
    pass


def covariance(x: np.ndarray, y: np.ndarray, ddof: int = 0) -> float:
    """
    Covariance measures whether x and y tend to move together (positive),
    move oppositely (negative), or show no consistent relationship
    (near zero):

        cov(x, y) = (1/(n - ddof)) * sum((x_i - mean(x)) * (y_i - mean(y)))

    Same ddof convention 05-expectation-covariance's sample_variance uses
    (in fact, covariance(x, x, ddof) is exactly sample_variance(x, ddof)).
    """
    pass


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    """
    Correlation rescales covariance into a unitless number in [-1, 1],
    by dividing out each variable's own spread:

        corr(x, y) = cov(x, y) / (std(x) * std(y))
    """
    pass
