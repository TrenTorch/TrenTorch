import numpy as np


def gradient_noise_scale(per_example_grads):
    g = np.asarray(per_example_grads, dtype=float)
    n = g.shape[0]
    mean = g.mean(axis=0)
    trace = ((g - mean) ** 2).sum() / (n - 1)
    return float(trace / (mean @ mean))


def steps_to_target(batch_size, s_min, b_crit):
    return float(s_min * (1.0 + b_crit / batch_size))
