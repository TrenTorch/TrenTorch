def combined_loss(hard_ce, soft_ce, alpha):
    """
    hard_ce: cross-entropy against the true labels
    soft_ce: cross-entropy against the teacher's soft targets
    alpha: weight on the soft loss, in [0, 1]

    Returns:
        alpha * soft_ce + (1 - alpha) * hard_ce.
    """
    # TODO: Blend the two losses with weight alpha (see Theory).
    pass
