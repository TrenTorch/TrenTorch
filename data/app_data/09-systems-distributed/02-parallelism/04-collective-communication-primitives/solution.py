import numpy as np


def all_reduce_sum(worker_arrays: list) -> list:
    total = sum(worker_arrays)
    return [total.copy() for _ in worker_arrays]


def all_gather(worker_shards: list) -> list:
    full = np.concatenate(worker_shards, axis=0)
    return [full.copy() for _ in worker_shards]


def reduce_scatter_sum(worker_arrays: list) -> list:
    total = sum(worker_arrays)
    return list(np.array_split(total, len(worker_arrays)))
