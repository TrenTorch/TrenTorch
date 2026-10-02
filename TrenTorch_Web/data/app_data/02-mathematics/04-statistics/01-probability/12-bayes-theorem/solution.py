def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    return (likelihood * prior) / evidence


def posterior_binary(
    prior_h: float, likelihood_e_given_h: float, likelihood_e_given_not_h: float
) -> float:
    evidence = likelihood_e_given_h * prior_h + likelihood_e_given_not_h * (1.0 - prior_h)
    return bayes_theorem(prior_h, likelihood_e_given_h, evidence)
