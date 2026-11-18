import numpy as np


def compute_cooperative_value(individual_values, shared_reward, weight=1.0):
    """
    Compute cooperative multi-agent value.

    Args:
        individual_values: list of value estimates from each agent
        shared_reward: reward shared by all agents
        weight: weight on shared reward component

    Returns:
        cooperative_value: combined value
    """
    individual_values = np.array(individual_values, dtype=np.float32)

    # Sum individual values
    individual_component = np.sum(individual_values)

    # Add shared reward component
    cooperative_value = individual_component + weight * shared_reward

    return float(cooperative_value)
