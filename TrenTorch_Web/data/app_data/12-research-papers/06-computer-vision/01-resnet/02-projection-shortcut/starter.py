def needs_projection(c_in, c_out, stride):
    """
    c_in: number of input channels to a residual block
    c_out: number of output channels of the block
    stride: stride of the block's first convolution

    Returns:
        True if the identity shortcut cannot be added directly and needs a 1x1 projection.
    """
    # TODO: Return True when channels change or the spatial size changes (see Theory).
    pass
