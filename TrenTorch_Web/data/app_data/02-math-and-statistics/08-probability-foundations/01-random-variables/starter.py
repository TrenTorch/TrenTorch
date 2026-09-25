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
