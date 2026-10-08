import numpy as np


def accumulate_preconditioners(L, R, G):
    return L + G @ G.T, R + G.T @ G
