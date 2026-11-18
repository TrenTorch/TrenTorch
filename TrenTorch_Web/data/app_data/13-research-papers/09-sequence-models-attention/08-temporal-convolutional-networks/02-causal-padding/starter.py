def causal_padding(kernel, dilation):
    """
    kernel: kernel size of the causal convolution
    dilation: dilation factor of the layer

    Returns:
        The number of zeros to pad on the left so the output at t depends only on inputs at or before t.
    """
    # TODO: Pad by the span the dilated kernel reaches into the past (see Theory).
    pass
