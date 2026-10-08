import numpy as np


def cascade_augment(X, class_vectors):
    """
    X: original features, shape (n, d)
    class_vectors: class vector for each sample from the previous layer, shape (n, c)

    Returns:
        The features for the next layer: X and class_vectors side by side, shape (n, d + c).
    """
    # TODO: Concatenate the features and the class vectors column-wise (see Theory).
    pass
