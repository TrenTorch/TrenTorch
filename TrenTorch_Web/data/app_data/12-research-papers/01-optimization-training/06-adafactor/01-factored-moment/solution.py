import numpy as np


def factored_second_moment(row, col):
    return np.outer(row, col) / np.sum(row)
