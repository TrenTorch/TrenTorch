def mixup_loss(loss_a, loss_b, lam):
    """
    loss_a: loss of the model's output against the first label
    loss_b: loss of the model's output against the second label
    lam: mixing weight in [0, 1]

    Returns:
        lam * loss_a + (1 - lam) * loss_b.
    """
    # TODO: Combine the two losses with the mixing weight (see Theory).
    pass
