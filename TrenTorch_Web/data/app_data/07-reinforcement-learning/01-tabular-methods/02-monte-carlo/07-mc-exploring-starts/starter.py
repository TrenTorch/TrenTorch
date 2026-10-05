import numpy as np


def mc_exploring_starts(env_step, num_episodes, gamma, num_states=10, num_actions=4, seed=None):
    """
    Monte Carlo control with exploring starts.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes to run
        gamma: discount factor
        num_states: number of possible states
        num_actions: number of possible actions
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: best_action}
    """
    pass
