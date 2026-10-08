def xgb_split_gain(GL, HL, GR, HR, lam, gamma):
    """
    GL, HL: gradient and hessian sums in the left child
    GR, HR: gradient and hessian sums in the right child
    lam: L2 regularization on leaf weights
    gamma: complexity penalty per leaf

    Returns:
        The gain from splitting the parent into the two children, from Theory.
    """
    # TODO: Compute the parent-minus-children score change and subtract gamma (see Theory).
    pass
