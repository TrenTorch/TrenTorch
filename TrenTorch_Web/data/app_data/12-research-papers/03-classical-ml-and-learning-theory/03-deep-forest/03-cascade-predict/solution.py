import numpy as np


def cascade_predict(forest_probas):
    avg = np.mean(np.stack(forest_probas), axis=0)
    return avg.argmax(axis=1)
