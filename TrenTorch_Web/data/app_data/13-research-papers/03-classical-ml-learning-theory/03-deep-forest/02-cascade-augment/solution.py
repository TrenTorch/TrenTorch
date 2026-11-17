import numpy as np


def cascade_augment(X, class_vectors):
    return np.hstack([np.asarray(X), np.asarray(class_vectors)])
