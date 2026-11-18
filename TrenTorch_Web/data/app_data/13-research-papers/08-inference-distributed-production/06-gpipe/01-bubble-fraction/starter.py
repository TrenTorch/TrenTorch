def pipeline_bubble_fraction(stages, micro):
    """
    stages: number of pipeline stages (devices)
    micro: number of micro-batches per step

    Returns:
        The fraction of time devices sit idle at the start and end of a step: (S - 1) / (M + S - 1).
    """
    # TODO: Compute the idle fraction from the number of stages and micro-batches (see Theory).
    pass
