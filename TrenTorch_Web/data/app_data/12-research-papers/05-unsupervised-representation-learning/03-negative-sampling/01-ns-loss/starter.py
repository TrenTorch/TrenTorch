import numpy as np


def negative_sampling_loss(v_c, u_o, U_neg):
    """
    v_c: input embedding of the center word, shape (d,)
    u_o: output embedding of the true context word, shape (d,)
    U_neg: output embeddings of k sampled negative words, shape (k, d)

    Returns:
        -log sigma(u_o . v_c) - sum_n log sigma(-u_n . v_c), as a float.
    """
    # TODO: Score the positive pair and each negative pair with the logistic loss (see Theory).
    pass
