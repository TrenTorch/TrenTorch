import numpy as np


def identity_path_gradient(grad_out, jac_f):
    grad_out = np.asarray(grad_out, dtype=float)
    return grad_out + grad_out @ jac_f
