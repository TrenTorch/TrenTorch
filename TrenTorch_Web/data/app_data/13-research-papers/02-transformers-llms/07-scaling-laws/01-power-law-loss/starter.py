import numpy as np


def power_law_loss(N, N_c, alpha):
    """
    N: number of model parameters (positive, scalar or array)
    N_c: a scale constant (positive)
    alpha: the power-law exponent (positive)

    Returns:
        (N_c / N) ** alpha, the predicted loss term from Kaplan et al.
    """
    # TODO: Compute the power law from Theory.
    pass
