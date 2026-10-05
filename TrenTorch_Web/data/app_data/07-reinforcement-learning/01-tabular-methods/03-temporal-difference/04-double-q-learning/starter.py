import numpy as np


def double_q_learning(env_step, num_episodes, epsilon, gamma, alpha, seed=None):
    """
    Double Q-Learning off-policy TD control.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes
        epsilon: exploration rate
        gamma: discount factor
        alpha: learning rate
        seed: random seed

    Returns:
        Q: dict {(state, action): estimated_value}
        policy: dict {state: best_action}
    """
    pass
