import numpy as np


def marginal_x(joint: np.ndarray) -> np.ndarray:
    return joint.sum(axis=1)


def marginal_y(joint: np.ndarray) -> np.ndarray:
    return joint.sum(axis=0)


def conditional_x_given_y(joint: np.ndarray, y_index: int) -> np.ndarray:
    column = joint[:, y_index]
    return column / column.sum()
