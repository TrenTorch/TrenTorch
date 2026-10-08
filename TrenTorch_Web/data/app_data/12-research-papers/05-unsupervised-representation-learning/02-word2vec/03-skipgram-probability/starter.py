import numpy as np


def skipgram_probability(v_c, U, o):
    """
    v_c: input embedding of the center word, shape (d,)
    U: output embeddings for every vocabulary word, shape (V, d)
    o: index of the observed context word

    Returns:
        P(o | c) = softmax(U v_c)[o], as a float.
    """
    # TODO: Score every vocabulary word against v_c, then take the softmax probability of o (see Theory).
    pass
