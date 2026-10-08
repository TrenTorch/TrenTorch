def receptive_field_stack(n, k=3):
    """
    n: number of stacked stride-1 convolutions
    k: kernel size of each convolution

    Returns:
        The receptive field of one output unit: 1 + n * (k - 1).
    """
    # TODO: Grow the receptive field by k - 1 per layer, starting from one pixel (see Theory).
    pass
