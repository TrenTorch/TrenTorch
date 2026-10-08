def attention_flops(n, d, causal=False):
    """
    n: sequence length
    d: head dimension
    causal: whether the causal mask halves the work

    Returns:
        The floating-point operations of one attention head's forward pass.
    """
    # TODO: Count the two matrix products, and halve the result for causal masks (see Theory).
    pass
