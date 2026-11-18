import numpy as np


def conv1x1(x, W, b):
    return x @ W.T + b
