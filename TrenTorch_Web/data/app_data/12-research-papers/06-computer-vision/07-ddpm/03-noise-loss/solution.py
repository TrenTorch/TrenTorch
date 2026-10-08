import numpy as np


def noise_prediction_loss(eps, eps_pred):
    return float(np.mean((np.asarray(eps, dtype=float) - np.asarray(eps_pred, dtype=float)) ** 2))
