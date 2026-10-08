import numpy as np


def kl_std_normal(mu, logvar):
    mu = np.asarray(mu, dtype=float)
    logvar = np.asarray(logvar, dtype=float)
    return float(-0.5 * np.sum(1 + logvar - mu**2 - np.exp(logvar)))
