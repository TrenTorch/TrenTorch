import math


def cosine_lr(t_cur, T_i, eta_min, eta_max):
    """
    t_cur: steps since the last restart; T_i: length of the current cycle
    eta_min, eta_max: learning rate bounds

    Returns:
        The cosine-annealed learning rate for the position in the cycle.
    """
    # TODO: Anneal from eta_max to eta_min along a half cosine over the cycle (see Theory).
    pass
