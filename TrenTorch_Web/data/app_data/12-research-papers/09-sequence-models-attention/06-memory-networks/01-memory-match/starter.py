import numpy as np


def memory_match(u, M):
    """
    u: question embedding, shape (d,)
    M: memory embeddings, one row per stored sentence, shape (n, d)

    Returns:
        The match score of each memory with the question, shape (n,).
    """
    # TODO: Compute the dot product of the question with each memory row (see Theory).
    pass
