import numpy as np


def tensor_parallel_matmul(x, shards):
    """
    x: input activations, shape (n, d_in), replicated on every device
    shards: column blocks of the weight, each of shape (d_in, d_out // world)

    Returns:
        The full output x @ W, shape (n, d_out), assembled from the per-device results.
    """
    # TODO: Multiply x by each shard and concatenate the results along the output axis (see Theory).
    pass
