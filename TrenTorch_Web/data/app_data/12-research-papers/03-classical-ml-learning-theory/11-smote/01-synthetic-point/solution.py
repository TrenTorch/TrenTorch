import numpy as np


def smote_point(x, neighbor, u):
    x = np.asarray(x, dtype=float)
    return x + u * (np.asarray(neighbor, dtype=float) - x)
