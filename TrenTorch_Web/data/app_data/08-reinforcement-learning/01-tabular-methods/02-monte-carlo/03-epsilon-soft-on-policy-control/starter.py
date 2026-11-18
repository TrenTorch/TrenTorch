import numpy as np


def epsilon_soft_mc_control(env_step, num_episodes, epsilon, gamma, seed=None):
    """
    Epsilon-soft on-policy MC control.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes to run
        epsilon: exploration probability
        gamma: discount factor
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: best_action}
    """
    pass
