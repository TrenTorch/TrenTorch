import numpy as np


def precondition_diag(L, G, R):
    return (L[:, None] ** -0.25) * G * (R[None, :] ** -0.25)
