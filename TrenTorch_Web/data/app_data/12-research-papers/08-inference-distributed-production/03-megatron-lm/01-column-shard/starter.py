import numpy as np


def column_shard(W, world):
    """
    W: weight matrix, shape (d_in, d_out) with d_out divisible by world
    world: number of tensor-parallel devices

    Returns:
        A list of world column blocks, each of shape (d_in, d_out // world).
    """
    # TODO: Split the weight matrix into equal column blocks, one per device (see Theory).
    pass
