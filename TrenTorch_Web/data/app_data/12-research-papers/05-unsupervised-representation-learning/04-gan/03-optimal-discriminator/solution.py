import numpy as np


def optimal_discriminator(p_data, p_model):
    p_data = np.asarray(p_data, dtype=float)
    p_model = np.asarray(p_model, dtype=float)
    return p_data / (p_data + p_model)
