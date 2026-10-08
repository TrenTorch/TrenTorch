import numpy as np


def linear_shap(w, x, mean):
    """
    w: weights of a linear model, shape (n,)
    x: the input to explain, shape (n,)
    mean: the feature means over the background data, shape (n,)

    Returns:
        The SHAP value of each feature for the linear model, w * (x - mean).
    """
    # TODO: Multiply each weight by the feature's deviation from its mean (see Theory).
    pass
