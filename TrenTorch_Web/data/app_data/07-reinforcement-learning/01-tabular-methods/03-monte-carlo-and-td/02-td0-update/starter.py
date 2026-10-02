import numpy as np


def td0_update(V: np.ndarray, state: int, reward: float, next_state: int,
               alpha: float, gamma: float, done: bool = False) -> np.ndarray:
    """
    V: (n_states,) current value estimates.
    state, next_state: integer state indices.
    reward: reward received on the transition.
    alpha: step size. gamma: discount factor.
    done: True if next_state is terminal.

    Returns:
        a copy of V with V[state] updated by the TD(0) rule.
    """
    # TODO: Build the TD target and move V[state] towards it.
    pass
