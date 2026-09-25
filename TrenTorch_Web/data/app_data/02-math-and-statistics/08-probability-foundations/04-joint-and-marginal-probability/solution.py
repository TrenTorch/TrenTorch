import numpy as np


def joint_from_independent(marginal_x, marginal_y):
    marginal_x = np.asarray(marginal_x, dtype=float)
    marginal_y = np.asarray(marginal_y, dtype=float)
    return np.outer(marginal_x, marginal_y)


def marginalize(joint, axis):
    joint = np.asarray(joint, dtype=float)
    return joint.sum(axis=axis)
