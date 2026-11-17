import numpy as np


def best_of_n_index(scores):
    return int(np.argmax(scores))
