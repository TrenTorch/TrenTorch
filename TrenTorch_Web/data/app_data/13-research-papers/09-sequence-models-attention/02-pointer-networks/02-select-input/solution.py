import numpy as np


def select_input(scores, inputs):
    return inputs[int(np.argmax(scores))]
