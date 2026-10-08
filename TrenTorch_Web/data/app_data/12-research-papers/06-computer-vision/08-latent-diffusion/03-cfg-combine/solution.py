import numpy as np


def cfg_combine(eps_u, eps_c, w):
    eps_u = np.asarray(eps_u, dtype=float)
    eps_c = np.asarray(eps_c, dtype=float)
    return eps_u + w * (eps_c - eps_u)
