import numpy as np


def make_lm_windows(token_ids, block_size, stride):
    ids = np.asarray(token_ids)
    n = len(ids)
    if n < block_size + 1:
        empty = np.zeros((0, block_size), dtype=ids.dtype)
        return empty, empty.copy()
    num = (n - block_size - 1) // stride + 1
    starts = np.arange(num) * stride
    grid = starts[:, None] + np.arange(block_size)[None, :]
    return ids[grid], ids[grid + 1]
