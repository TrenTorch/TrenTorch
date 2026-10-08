def ordered_target_encoding(cats, ys, prior, a=1.0):
    """
    cats: category of each sample, in training order
    ys: label of each sample, in the same order
    prior: a prior guess for the target mean
    a: weight given to the prior

    Returns:
        For each sample, the target statistic computed only from earlier samples
        with the same category, so a sample never sees its own label.
    """
    # TODO: Walk the samples in order, encoding each one before adding its label (see Theory).
    pass
