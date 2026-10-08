import numpy as np


def optimal_discriminator(p_data, p_model):
    """
    p_data: data density at each point, nonnegative
    p_model: generator density at each point, nonnegative, not both zero

    Returns:
        D*(x) = p_data(x) / (p_data(x) + p_model(x)), the best possible discriminator.
    """
    # TODO: Return the density ratio from Theory, element-wise.
    pass
