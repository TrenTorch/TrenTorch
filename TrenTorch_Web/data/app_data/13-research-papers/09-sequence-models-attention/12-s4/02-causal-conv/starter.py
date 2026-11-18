def causal_conv_from_kernel(K, x):
    """
    K: impulse response, K[k] applied to the input k steps back
    x: input sequence

    Returns:
        The causal convolution y_t = sum_k K[k] x[t - k], with zeros before the start.
    """
    # TODO: Sum kernel taps times the inputs that many steps back, for each output step (see Theory).
    pass
