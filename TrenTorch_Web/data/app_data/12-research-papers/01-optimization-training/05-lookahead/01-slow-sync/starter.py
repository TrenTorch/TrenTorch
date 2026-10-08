def lookahead_sync(slow, fast, alpha):
    """
    slow: slow weights before the sync; fast: fast weights after k inner steps
    alpha: interpolation factor in (0, 1]

    Returns:
        The new slow weights, slow + alpha * (fast - slow).
    """
    # TODO: Move the slow weights a fraction alpha toward the fast weights (see Theory).
    pass
