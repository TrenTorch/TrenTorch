def clip_scale(norm, threshold):
    """
    norm: the gradient norm; threshold: maximum allowed norm

    Returns:
        The multiplier min(1, threshold / norm) applied to the gradient.
    """
    # TODO: Take the smaller of one and threshold over norm (see Theory).
    pass
