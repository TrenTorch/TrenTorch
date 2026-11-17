import numpy as np


def lamb_trust_ratio(w, r):
    return float(np.linalg.norm(w) / np.linalg.norm(r))
