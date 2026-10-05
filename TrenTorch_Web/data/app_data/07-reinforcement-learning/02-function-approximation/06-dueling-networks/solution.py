import numpy as np


def combine_value_advantage(value, advantage):
    """
    Combine value and advantage streams into Q-values.

    Args:
        value: scalar value V(s)
        advantage: vector of advantages A(s,a)

    Returns:
        q_values: Q(s,a) for each action
    """
    value = float(value)
    advantage = np.array(advantage, dtype=np.float32)

    # Advantage centering: A - mean(A)
    centered_advantage = advantage - np.mean(advantage)

    # Q(s,a) = V(s) + (A(s,a) - mean_a A(s,a))
    q_values = value + centered_advantage

    return q_values
