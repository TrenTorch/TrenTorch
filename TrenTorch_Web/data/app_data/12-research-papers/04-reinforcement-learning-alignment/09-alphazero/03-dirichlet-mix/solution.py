import numpy as np


def dirichlet_mix(P, noise, eps):
    P = np.asarray(P, dtype=float)
    noise = np.asarray(noise, dtype=float)
    return (1 - eps) * P + eps * noise
