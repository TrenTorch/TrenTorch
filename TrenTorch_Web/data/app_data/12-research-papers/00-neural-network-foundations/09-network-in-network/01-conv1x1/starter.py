import numpy as np


def conv1x1(x, W, b):
    """
    x: feature map, shape (H, W, C)
    W: channel-mixing weights, shape (C_out, C)
    b: bias, shape (C_out,)

    Returns:
        A feature map of shape (H, W, C_out), where each spatial position is
        mapped by the same linear layer over channels.
    """
    # TODO: Apply the same channel-mixing linear map at every spatial position.
    pass
