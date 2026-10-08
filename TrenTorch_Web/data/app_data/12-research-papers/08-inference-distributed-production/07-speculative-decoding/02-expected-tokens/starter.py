def expected_tokens_accepted(alpha, gamma):
    """
    alpha: per-token acceptance rate, in [0, 1)
    gamma: number of tokens drafted per step

    Returns:
        The expected number of tokens produced per target pass: (1 - alpha^(gamma+1)) / (1 - alpha).
    """
    # TODO: Sum the geometric series of accepted-prefix lengths (see Theory).
    pass
