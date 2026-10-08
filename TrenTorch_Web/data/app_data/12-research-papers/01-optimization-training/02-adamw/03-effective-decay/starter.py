def effective_decay(lr, wd, steps):
    """
    lr: learning rate; wd: decoupled weight decay coefficient
    steps: number of optimizer steps

    Returns:
        The fraction of the original weights left after the given steps of decay alone.
    """
    # TODO: Compound the per-step shrink factor over the steps (see Theory).
    pass
