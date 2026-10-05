import math


def is_valid_pmf(probabilities):
    """
    probabilities: list/tuple of floats, one per outcome of a discrete
        random variable.

    Returns:
        True if `probabilities` is a valid probability mass function:
        every value is non-negative AND they sum to 1 (within 1e-9).
    """
    # TODO: Implement the two PMF axioms from Theory.
    pass


def expected_value_discrete(outcomes, probabilities):
    """
    outcomes: list/tuple of numbers, the values a discrete random
        variable X can take.
    probabilities: list/tuple of floats, P(X = outcomes[i]) for each i,
        same length as outcomes.

    Returns:
        E[X] = sum(outcome * probability), from Theory.
    """
    # TODO: Implement the weighted-sum definition of expectation.
    pass


def binomial_pmf(n, p, k):
    """
    n: number of independent trials (positive int)
    p: probability of success on each trial (float in [0, 1])
    k: number of successes to compute the probability of (int in [0, n])

    Returns:
        P(X = k) for X ~ Binomial(n, p), from Theory.
    """
    # TODO: Implement C(n, k) * p**k * (1-p)**(n-k) from Theory.
    pass


def uniform_pdf(x, a, b):
    """
    x: point to evaluate the density at
    a, b: the interval's lower and upper bounds (a < b)

    Returns:
        The value of the continuous Uniform(a, b) density at x: 1/(b-a)
        inside [a, b], and 0 outside it.
    """
    # TODO: Implement the piecewise density from Theory.
    pass
