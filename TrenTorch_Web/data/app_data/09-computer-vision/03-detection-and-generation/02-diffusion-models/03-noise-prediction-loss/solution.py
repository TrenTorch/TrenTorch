import numpy as np


def noise_prediction_loss(eps_pred, eps):
    return float(np.mean((np.asarray(eps_pred, dtype=float) - np.asarray(eps, dtype=float)) ** 2))


def predict_x0(x_t, eps_pred, t, alpha_bars):
    ab = alpha_bars[t]
    return (np.asarray(x_t, dtype=float) - np.sqrt(1.0 - ab) * np.asarray(eps_pred, dtype=float)) / np.sqrt(ab)
