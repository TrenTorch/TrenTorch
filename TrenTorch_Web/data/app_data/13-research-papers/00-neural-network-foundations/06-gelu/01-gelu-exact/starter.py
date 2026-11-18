import numpy as np


def gelu_exact(x):
    """
    x: input activations (NumPy array)

    Returns:
        x * Phi(x), where Phi is the standard Gaussian CDF, element-wise.
    """
    # TODO: Multiply x by the standard normal CDF, computed with math.erf (see Theory).
    pass
