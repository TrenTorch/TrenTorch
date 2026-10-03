import numpy as np


def ipo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, tau):
    h = (np.asarray(pi_chosen, float) - np.asarray(ref_chosen, float)) - (
        np.asarray(pi_rejected, float) - np.asarray(ref_rejected, float)
    )
    return float(((h - 1.0 / (2.0 * tau)) ** 2).mean())


def simpo_loss(pi_chosen, pi_rejected, len_chosen, len_rejected, beta, gamma):
    z = beta * (
        np.asarray(pi_chosen, float) / np.asarray(len_chosen, float)
        - np.asarray(pi_rejected, float) / np.asarray(len_rejected, float)
    ) - gamma
    return float(np.logaddexp(0.0, -z).mean())
