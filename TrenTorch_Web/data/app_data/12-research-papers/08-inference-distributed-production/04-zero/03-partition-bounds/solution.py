import numpy as np


def partition_bounds(total, N, rank):
    sizes = [len(c) for c in np.array_split(np.arange(total), N)]
    start = sum(sizes[:rank])
    return (start, start + sizes[rank])
