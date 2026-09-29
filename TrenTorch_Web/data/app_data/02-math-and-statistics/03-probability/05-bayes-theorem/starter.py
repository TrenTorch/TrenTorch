def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    """
    Bayes' theorem in its rawest form:

        posterior = (likelihood * prior) / evidence

    All three inputs are already computed elsewhere; this function is
    purely the combination rule.
    """
    pass


def posterior_binary(
    prior_h: float, likelihood_e_given_h: float, likelihood_e_given_not_h: float
) -> float:
    """
    The common case: a binary hypothesis H (true/false), and you're
    given P(H) (the prior), P(evidence | H), and P(evidence | not H).
    Compute P(evidence) yourself first (there are only two ways the
    evidence could have occurred: H is true, or H is false), then call
    bayes_theorem with the pieces you now have.
    """
    pass
