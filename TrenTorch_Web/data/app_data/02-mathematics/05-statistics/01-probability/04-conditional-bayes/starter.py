import numpy as np
import math


def marginal_x(joint: np.ndarray) -> np.ndarray:
    """
    `joint` is a 2D array where joint[i, j] = P(X=i, Y=j). The marginal
    distribution of X alone, P(X=i), sums out every value of Y:

        P(X=i) = sum_j(P(X=i, Y=j))
    """
    pass


def marginal_y(joint: np.ndarray) -> np.ndarray:
    """
    Same idea as marginal_x, summed the other way: P(Y=j) sums out
    every value of X.
    """
    pass


def conditional_x_given_y(joint: np.ndarray, y_index: int) -> np.ndarray:
    """
    P(X | Y=y_index): restrict to the single column where Y=y_index,
    then renormalize so it sums to 1 on its own (a valid probability
    distribution over X, not just an unnormalized slice of `joint`).
    """
    pass


def joint_via_chain_rule(p_x, p_y_given_x, p_z_given_xy):
    """
    p_x: P(X = x), a float
    p_y_given_x: P(Y = y | X = x), a float
    p_z_given_xy: P(Z = z | X = x, Y = y), a float

    Returns:
        The joint P(X=x, Y=y, Z=z), factorized via the chain rule from
        Theory: P(X) * P(Y|X) * P(Z|X,Y).
    """
    # TODO: Implement the three-factor chain rule from Theory.
    pass


def chain_rule_general(conditionals):
    """
    conditionals: list of floats [P(X_1), P(X_2|X_1), P(X_3|X_1,X_2), ...],
        one factor per variable in a fixed ordering.

    Returns:
        The full joint probability of all variables, as the product of
        every factor in `conditionals`, from Theory.
    """
    # TODO: Implement the product of all conditionals from Theory.
    pass


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
