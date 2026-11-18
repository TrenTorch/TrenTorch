import numpy as np


def logdet_1x1(W, h, w):
    """
    W: the channel-mixing matrix of an invertible 1x1 convolution, shape (C, C)
    h, w: spatial height and width of the feature map

    Returns:
        The log absolute determinant of the layer's Jacobian: h * w * log|det W|, as a float.
    """
    # TODO: Use the log-determinant of W, scaled by the number of spatial positions (see Theory).
    pass
