import numpy as np


def joint_from_independent(marginal_x, marginal_y):
    marginal_x = np.asarray(marginal_x, dtype=float)
    marginal_y = np.asarray(marginal_y, dtype=float)
    return np.outer(marginal_x, marginal_y)


def marginalize(joint, axis):
    joint = np.asarray(joint, dtype=float)
    return joint.sum(axis=axis)


def is_independent(joint, tol=1e-9):
    joint = np.asarray(joint, dtype=float)
    marginal_x = joint.sum(axis=1)
    marginal_y = joint.sum(axis=0)
    expected = np.outer(marginal_x, marginal_y)
    return bool(np.allclose(joint, expected, atol=tol))


def conditional_pmf_given_y(joint, y_index):
    joint = np.asarray(joint, dtype=float)
    marginal_y = joint.sum(axis=0)
    return joint[:, y_index] / marginal_y[y_index]
