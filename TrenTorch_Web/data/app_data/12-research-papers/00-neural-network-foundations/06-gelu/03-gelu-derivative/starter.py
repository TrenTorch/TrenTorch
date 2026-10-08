import numpy as np


def gelu_derivative(x):
    """
    x: input activations (NumPy array)

    Returns:
        d/dx [x * Phi(x)] = Phi(x) + x * phi(x), element-wise, where phi is the
        standard normal density.
    """
    # TODO: Compute Phi(x) and phi(x) and combine them as in Theory.
    pass
