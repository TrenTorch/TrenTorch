import numpy as np


def reparameterize(mu, logvar, eps):
    return mu + np.exp(0.5 * logvar) * eps
