import math


def workers_for_batch(batch, per_worker):
    """
    batch: total global minibatch size; per_worker: examples each worker processes per step

    Returns:
        The number of workers needed to cover the batch, rounding up.
    """
    # TODO: Divide the batch by the per-worker share, rounding up (see Theory).
    pass
