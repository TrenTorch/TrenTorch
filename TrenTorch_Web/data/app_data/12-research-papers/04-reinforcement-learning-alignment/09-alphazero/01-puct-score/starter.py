import math


def puct_score(Q, P, N_parent, N_child, c):
    """
    Q: mean value of the child from simulations so far
    P: prior probability of the move from the policy network
    N_parent: visit count of the parent node
    N_child: visit count of the child node
    c: exploration constant

    Returns:
        The PUCT selection score Q + c * P * sqrt(N_parent) / (1 + N_child).
    """
    # TODO: Add the exploration bonus to the value (see Theory).
    pass
