import numpy as np


def linear_shap(w, x, mean):
    return np.asarray(w, dtype=float) * (np.asarray(x, dtype=float) - np.asarray(mean, dtype=float))
