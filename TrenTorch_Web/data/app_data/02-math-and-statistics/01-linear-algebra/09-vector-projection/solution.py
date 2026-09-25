import numpy as np


def project(a, b):
    scalar = (a @ b) / (b @ b)
    return scalar * b


def orthogonal_component(a, b):
    return a - project(a, b)
