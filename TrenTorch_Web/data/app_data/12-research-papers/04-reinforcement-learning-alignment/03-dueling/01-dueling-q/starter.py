import numpy as np


def dueling_q(V, A):
    """
    V: state value, a scalar
    A: advantage for each action, shape (num_actions,)

    Returns:
        Q(s, a) = V + A(a) - mean(A), shape (num_actions,).
    """
    # TODO: Combine the value and the mean-subtracted advantages (see Theory).
    pass
