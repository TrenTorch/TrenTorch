import math


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
