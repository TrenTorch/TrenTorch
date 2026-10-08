def lora_param_count(d_in, d_out, r):
    """
    d_in: input dimension of the weight matrix
    d_out: output dimension of the weight matrix
    r: LoRA rank

    Returns:
        The number of trainable parameters in the LoRA update, r * (d_in + d_out).
    """
    # TODO: Count the entries of A (r by d_in) and B (d_out by r) (see Theory).
    pass
