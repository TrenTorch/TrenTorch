import math


def joint_via_chain_rule(p_x, p_y_given_x, p_z_given_xy):
    return p_x * p_y_given_x * p_z_given_xy


def chain_rule_general(conditionals):
    return math.prod(conditionals)
