def tcn_receptive_field(kernel, levels):
    """
    kernel: kernel size of each causal convolution
    levels: number of layers, with dilation 2^i at layer i

    Returns:
        The receptive field 1 + (kernel - 1) * (2^levels - 1).
    """
    # TODO: Sum the dilated spans over the levels (see Theory).
    pass
