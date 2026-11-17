import numpy as np


def softmax_probabilities(q_values: np.ndarray, temperature: float) -> np.ndarray:
    """
    q_values: (n_arms,) estimated values.
    temperature: positive float.

    Returns:
        (n_arms,) probabilities summing to 1.
    """
    # TODO: Numerically stable softmax of q_values / temperature.
    pass
