def weighted_total_loss(main, aux, w=0.3):
    """
    main: loss of the final classifier
    aux: loss of an auxiliary classifier attached to an intermediate layer
    w: weight on the auxiliary loss (0.3 in the paper)

    Returns:
        The training loss main + w * aux.
    """
    # TODO: Add the auxiliary loss, scaled by w, to the main loss (see Theory).
    pass
