def xgb_leaf_weight(G, H, lam):
    """
    G: sum of first-order gradients of the samples in a leaf
    H: sum of second-order gradients (hessians) of those samples
    lam: L2 regularization on leaf weights

    Returns:
        The optimal leaf weight -G / (H + lam).
    """
    # TODO: Return the regularized Newton step from Theory.
    pass
