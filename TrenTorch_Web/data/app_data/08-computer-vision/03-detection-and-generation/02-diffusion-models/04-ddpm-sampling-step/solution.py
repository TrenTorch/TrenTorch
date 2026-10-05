import numpy as np


def ddpm_step(x_t, eps_pred, t, betas, alpha_bars, z):
    beta = betas[t]
    alpha = 1.0 - beta
    mean = (np.asarray(x_t, dtype=float) - beta / np.sqrt(1.0 - alpha_bars[t]) * np.asarray(eps_pred, dtype=float)) / np.sqrt(alpha)
    if t > 0:
        return mean + np.sqrt(beta) * np.asarray(z, dtype=float)
    return mean
