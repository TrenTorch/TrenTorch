def wavenet_receptive_field(dilations, kernel=2):
    """
    dilations: dilation factor of each causal convolution layer, in order
    kernel: kernel size of each layer

    Returns:
        The number of past samples one output depends on: 1 + sum((kernel - 1) * dilation).
    """
    # TODO: Add the span each dilated layer contributes to the receptive field (see Theory).
    pass
