import numpy as np


def ddpg_critic_target(r, gamma, done, q_next):
    """
    r: reward
    gamma: discount factor
    done: 1 if the episode ended, else 0
    q_next: target critic's value at the next state and the target actor's action

    Returns:
        The critic regression target r + gamma * (1 - done) * q_next.
    """
    # TODO: Bootstrap from the target critic unless the episode ended (see Theory).
    pass
