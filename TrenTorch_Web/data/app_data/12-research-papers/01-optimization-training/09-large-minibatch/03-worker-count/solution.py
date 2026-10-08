import math


def workers_for_batch(batch, per_worker):
    return math.ceil(batch / per_worker)
