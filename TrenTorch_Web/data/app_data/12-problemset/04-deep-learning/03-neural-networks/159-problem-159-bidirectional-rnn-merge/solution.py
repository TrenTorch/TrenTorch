import numpy as np

def solve(forward, backward):
    forward = np.asarray(forward)
    backward = np.asarray(backward)
    if forward.shape[:-1] != backward.shape[:-1]:
        raise ValueError("forward and backward states must share leading dimensions")
    return np.concatenate((forward, backward), axis=-1)
