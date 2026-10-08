import numpy as np


def switch_route(logits):
    """
    logits: router scores, shape (T, E), one row per token and E experts

    Returns:
        (idx, gate): the index of the top expert for each token, shape (T,), and
        that expert's softmax probability, shape (T,).
    """
    # TODO: Softmax the router logits, then pick the top expert and its probability (see Theory).
    pass
