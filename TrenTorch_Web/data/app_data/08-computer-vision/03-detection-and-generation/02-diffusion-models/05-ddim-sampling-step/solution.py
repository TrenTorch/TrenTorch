import numpy as np


def ddim_step(x_t, eps_pred, t, t_prev, alpha_bars):
    ab = alpha_bars[t]
    ab_prev = 1.0 if t_prev < 0 else alpha_bars[t_prev]
    x_t = np.asarray(x_t, dtype=float)
    eps_pred = np.asarray(eps_pred, dtype=float)
    x0_hat = (x_t - np.sqrt(1.0 - ab) * eps_pred) / np.sqrt(ab)
    return np.sqrt(ab_prev) * x0_hat + np.sqrt(1.0 - ab_prev) * eps_pred
