def gradual_warmup_lr(target, t, warmup):
    """
    target: the learning rate after warmup; t: current step (1-indexed); warmup: warmup length in steps

    Returns:
        The learning rate ramped linearly from near zero up to target over warmup steps, then held.
    """
    # TODO: Ramp the rate linearly over the warmup steps, then hold it at target (see Theory).
    pass
