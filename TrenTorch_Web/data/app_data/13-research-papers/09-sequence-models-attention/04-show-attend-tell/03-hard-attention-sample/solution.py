import numpy as np


def sample_hard_attention(alpha, rng):
    return int(rng.choice(len(alpha), p=np.asarray(alpha, dtype=float)))
