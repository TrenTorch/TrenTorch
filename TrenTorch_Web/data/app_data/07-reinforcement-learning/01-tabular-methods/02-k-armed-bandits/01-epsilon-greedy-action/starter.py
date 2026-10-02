import numpy as np


def epsilon_greedy_action(q_values: np.ndarray, epsilon: float, rng: np.random.Generator) -> int:
    """
    q_values: (n_arms,) current estimated value of each arm.
    epsilon: probability of exploring.
    rng: numpy Generator.

    Returns:
        the chosen arm index.
    """
    # TODO: Explore with probability epsilon, otherwise pick the best arm.
    pass
