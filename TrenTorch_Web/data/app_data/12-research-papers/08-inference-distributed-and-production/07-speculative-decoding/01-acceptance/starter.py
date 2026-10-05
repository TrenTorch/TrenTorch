def acceptance_prob(p, q):
    """
    p: target model's probability of a drafted token
    q: draft model's probability of the same token, positive

    Returns:
        The probability of accepting the drafted token, min(1, p / q).
    """
    # TODO: Take the ratio of the target and draft probabilities, capped at one (see Theory).
    pass
