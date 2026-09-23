def compound_scale(
    phi: int, alpha: float = 1.2, beta: float = 1.1, gamma: float = 1.15
) -> tuple[float, float, float]:
    """
    phi: a single non-negative integer "compound coefficient" the user
        picks to control how much bigger the scaled model should be
    alpha, beta, gamma: base per-step multipliers for depth, width, and
        input resolution respectively (EfficientNet's paper found
        alpha=1.2, beta=1.1, gamma=1.15 to work well, satisfying
        alpha * beta^2 * gamma^2 ~= 2)

    EfficientNet's compound scaling: instead of arbitrarily scaling only
    depth (more layers), or only width (more channels), or only
    resolution (bigger input images) -- the classic approach, and prone
    to diminishing returns when pushed on just one axis -- scale all
    three together, uniformly controlled by a single knob phi.

    Returns (depth_mult, width_mult, resolution_mult): multiply the
    base model's depth, width and input resolution by each of these,
    respectively, to get phi's scaled-up model.
    """
    # TODO: return (alpha ** phi, beta ** phi, gamma ** phi).
    pass
