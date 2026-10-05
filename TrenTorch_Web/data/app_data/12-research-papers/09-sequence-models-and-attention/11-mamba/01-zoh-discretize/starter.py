import math


def zoh_discretize(A, B, delta):
    """
    A: continuous-time state scalar (nonzero)
    B: continuous-time input scalar
    delta: step size (positive)

    Returns:
        (A_bar, B_bar), the zero-order-hold discretization exp(delta A) and (exp(delta A) - 1) B / A.
    """
    # TODO: Apply the zero-order-hold formulas for a scalar state (see Theory).
    pass
