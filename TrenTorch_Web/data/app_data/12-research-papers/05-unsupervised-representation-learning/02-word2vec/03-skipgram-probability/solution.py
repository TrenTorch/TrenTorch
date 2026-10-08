import numpy as np


def skipgram_probability(v_c, U, o):
    scores = U @ np.asarray(v_c, dtype=float)
    e = np.exp(scores - scores.max())
    return float((e / e.sum())[o])
