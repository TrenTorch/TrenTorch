import numpy as np


def all_reduce_sum(worker_arrays: list) -> list:
    """
    Every worker holds a SAME-SHAPE array (e.g. its own gradient).
    all-reduce combines them (here: sum) and gives EVERY worker the
    combined result -- the collective a DDP gradient sync actually is.
    """
    # TODO: sum all arrays elementwise, return a list with that same
    # sum given back to every worker.
    pass


def all_gather(worker_shards: list) -> list:
    """
    Every worker holds a DIFFERENT shard of something (e.g. its slice
    of an embedding table). all-gather concatenates every worker's
    shard (in rank order) and gives the FULL concatenation to every
    worker.
    """
    # TODO: concatenate worker_shards along axis 0, return a list with
    # that same full array given back to every worker.
    pass


def reduce_scatter_sum(worker_arrays: list) -> list:
    """
    Every worker holds a SAME-SHAPE array, like all-reduce's input --
    but instead of every worker getting the FULL combined result,
    reduce-scatter sums them and then splits the result, giving each
    worker only ITS OWN chunk (memory-efficient half of all-reduce).
    """
    # TODO: sum all arrays elementwise (like all_reduce_sum), then
    # np.array_split the sum into len(worker_arrays) chunks.
    pass
