import numpy as np


def enqueue(queue, new_keys, K):
    """
    queue: current queue of keys, shape (m, d)
    new_keys: keys from the current batch, shape (b, d)
    K: maximum queue length

    Returns:
        The queue after appending new_keys and dropping the oldest entries, keeping the last K rows.
    """
    # TODO: Append the new keys and keep only the most recent K (see Theory).
    pass
