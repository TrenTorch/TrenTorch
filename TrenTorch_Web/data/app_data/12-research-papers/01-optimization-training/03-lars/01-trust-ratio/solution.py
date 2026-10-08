import numpy as np


def trust_ratio(w, g, eta, wd):
    return eta * np.linalg.norm(w) / (np.linalg.norm(g) + wd * np.linalg.norm(w))
