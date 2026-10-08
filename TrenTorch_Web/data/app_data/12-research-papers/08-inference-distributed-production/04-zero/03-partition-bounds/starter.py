import numpy as np


def partition_bounds(total, N, rank):
    """
    total: number of elements to partition
    N: number of devices
    rank: the device whose shard is wanted, 0 to N - 1

    Returns:
        The half-open range (start, end) of the elements owned by that device.
    """
    # TODO: Work out the shard sizes and the offset where this rank's shard begins (see Theory).
    pass
