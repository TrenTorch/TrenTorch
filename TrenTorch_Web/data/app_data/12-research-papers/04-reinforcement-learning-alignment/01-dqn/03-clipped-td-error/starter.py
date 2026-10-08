import numpy as np


def clipped_td_error(td, c):
    """
    td: temporal-difference errors, target minus prediction (array or scalar)
    c: clipping bound (positive)

    Returns:
        The errors clipped to the interval [-c, c], element-wise.
    """
    # TODO: Clip each TD error to [-c, c] (see Theory).
    pass
