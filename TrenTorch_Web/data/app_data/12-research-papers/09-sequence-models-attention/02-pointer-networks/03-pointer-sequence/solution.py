import numpy as np


def pointer_argmax_sequence(scores_seq):
    return [int(i) for i in np.argmax(np.asarray(scores_seq, dtype=float), axis=1)]
