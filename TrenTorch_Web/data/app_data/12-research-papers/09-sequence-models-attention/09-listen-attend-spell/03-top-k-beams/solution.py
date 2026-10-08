import numpy as np


def top_k_beams(scores, k):
    order = np.argsort(-np.asarray(scores, dtype=float), kind="stable")
    return [int(i) for i in order[:k]]
