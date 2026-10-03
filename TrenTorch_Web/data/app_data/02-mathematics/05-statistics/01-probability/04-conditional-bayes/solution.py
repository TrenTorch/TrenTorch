import numpy as np
import math


def marginal_x(joint: np.ndarray) -> np.ndarray:
    return joint.sum(axis=1)


def marginal_y(joint: np.ndarray) -> np.ndarray:
    return joint.sum(axis=0)


def conditional_x_given_y(joint: np.ndarray, y_index: int) -> np.ndarray:
    column = joint[:, y_index]
    return column / column.sum()


def joint_via_chain_rule(p_x, p_y_given_x, p_z_given_xy):
    return p_x * p_y_given_x * p_z_given_xy


def chain_rule_general(conditionals):
    return math.prod(conditionals)


def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    return (likelihood * prior) / evidence


def posterior_binary(
    prior_h: float, likelihood_e_given_h: float, likelihood_e_given_not_h: float
) -> float:
    evidence = likelihood_e_given_h * prior_h + likelihood_e_given_not_h * (1.0 - prior_h)
    return bayes_theorem(prior_h, likelihood_e_given_h, evidence)
