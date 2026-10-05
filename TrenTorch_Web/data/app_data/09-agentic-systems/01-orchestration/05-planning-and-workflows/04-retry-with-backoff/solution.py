import random


def backoff_delays(n_retries, base, factor, cap, rng=None):
    capped = [min(cap, base * factor ** k) for k in range(n_retries)]
    if rng is None:
        return capped
    return [c * rng.random() for c in capped]


def total_wait(delays):
    return float(sum(delays))
