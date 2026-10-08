import math


def optimal_params_for_budget(flops):
    """
    flops: total training compute budget C

    Returns:
        The compute-optimal parameter count N, from C = 6 * N * (20 * N), i.e. N = sqrt(C / 120).
    """
    # TODO: Solve 6 * N * (20 * N) = C for N (see Theory).
    pass
