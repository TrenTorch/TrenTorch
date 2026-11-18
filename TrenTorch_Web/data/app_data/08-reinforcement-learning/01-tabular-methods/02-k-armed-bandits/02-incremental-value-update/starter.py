import numpy as np


def update_action_value(q_values: np.ndarray, counts: np.ndarray, action: int, reward: float) -> tuple:
    """
    q_values: (n_arms,) current estimates.
    counts: (n_arms,) times each arm has been pulled.
    action: index of the arm just pulled.
    reward: reward observed.

    Returns:
        (new_q_values, new_counts); inputs are left unchanged.
    """
    # TODO: Bump the count, then apply the incremental-mean update.
    pass
