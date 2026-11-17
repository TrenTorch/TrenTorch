import numpy as np


def greedy_action(q):
    return int(np.argmax(q))
