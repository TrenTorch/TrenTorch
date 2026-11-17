import numpy as np


def clip_symmetric_loss(logits):
    """
    logits: N x N similarity matrix, where the diagonal holds the matching pairs

    Returns:
        The average of the image-to-text and text-to-image cross-entropy losses, as a float.
    """
    # TODO: Compute the cross-entropy with diagonal targets in both directions and average (see Theory).
    pass
