import numpy as np


def noise_prediction_loss(eps, eps_pred):
    """
    eps: the noise that was added
    eps_pred: the network's prediction of that noise, same shape

    Returns:
        The mean squared error between the true and predicted noise, as a float.
    """
    # TODO: Average the squared difference between the true and predicted noise (see Theory).
    pass
