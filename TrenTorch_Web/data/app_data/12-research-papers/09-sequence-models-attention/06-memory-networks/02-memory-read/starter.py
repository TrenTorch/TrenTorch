import numpy as np


def memory_output(p, outputs):
    """
    p: attention over memories, shape (n,), summing to 1
    outputs: output embeddings of the memories, shape (n, d)

    Returns:
        The output vector o = sum_i p_i * outputs[i], shape (d,).
    """
    # TODO: Take the attention-weighted sum of the output embeddings (see Theory).
    pass
