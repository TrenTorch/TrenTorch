import numpy as np


def double_q_target(r, gamma, done, q_next_online, q_next_target):
    """
    r: reward
    gamma: discount factor
    done: 1 if the episode ended, else 0
    q_next_online: online network's Q-values at the next state, shape (A,)
    q_next_target: target network's Q-values at the next state, shape (A,)

    Returns:
        The Double DQN target: the online network picks the action, the target network evaluates it.
    """
    # TODO: Select the action with the online values, evaluate it with the target values (see Theory).
    pass
