import numpy as np


def select_ucb_action(q_values, counts, t, c):
    """
    Select an action using the Upper Confidence Bound (UCB) strategy.

    Args:
        q_values: array of shape (num_actions,) with estimated value of each action
        counts: array of shape (num_actions,) with visit count of each action
        t: current time step (integer >= 1)
        c: exploration constant (float > 0)

    Returns:
        int: selected action index
    """
    pass
