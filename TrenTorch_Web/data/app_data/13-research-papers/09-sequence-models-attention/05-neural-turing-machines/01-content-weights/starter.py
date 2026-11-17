import numpy as np


def content_weights(memory, key, beta):
    """
    memory: memory matrix, shape (N, M)
    key: query key vector, shape (M,)
    beta: sharpness of the focus (positive)

    Returns:
        A distribution over memory rows, softmax(beta * cosine similarity), shape (N,).
    """
    # TODO: Compute cosine similarity with each row, then a softmax with sharpness beta (see Theory).
    pass
