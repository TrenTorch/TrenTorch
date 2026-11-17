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
    q_values = np.asarray(q_values)
    counts = np.asarray(counts)

    # Compute UCB for each action
    # UCB(a) = Q(a) + c * sqrt(ln(t) / N(a))
    # If N(a) = 0, the bonus is infinite
    bonuses = np.where(
        counts > 0,
        c * np.sqrt(np.log(t) / counts),
        np.inf
    )
    ucb_values = q_values + bonuses

    return int(np.argmax(ucb_values))
