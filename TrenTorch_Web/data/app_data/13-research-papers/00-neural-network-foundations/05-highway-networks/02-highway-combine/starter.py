def highway_combine(x, h, t):
    """
    x: the layer input (carry path)
    h: the nonlinear transform of x (transform path)
    t: the gate, same shape as x, with values in [0, 1]

    Returns:
        h * t + x * (1 - t), element-wise.
    """
    # TODO: Blend the transform and carry paths with the gate (see Theory).
    pass
