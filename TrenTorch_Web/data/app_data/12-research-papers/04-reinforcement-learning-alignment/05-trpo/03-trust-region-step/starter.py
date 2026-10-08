import math


def trust_region_step_size(delta, quad):
    """
    delta: the KL step limit (positive)
    quad: the quadratic form g^T F^{-1} g, the curvature of the KL along the gradient (positive)

    Returns:
        The largest step length beta with (1/2) beta^2 quad = delta, namely sqrt(2 delta / quad).
    """
    # TODO: Solve (1/2) beta^2 quad = delta for beta (see Theory).
    pass
