def adam_update_moments(m, v, grad, beta1=0.9, beta2=0.999):
    """
    m: current first-moment estimate (running average of gradients)
    v: current second-moment estimate (running average of squared gradients)
    grad: the gradient at the current step (float or NumPy array)
    beta1, beta2: decay rates for the two running averages

    Returns:
        (new_m, new_v), the two moment estimates after folding in `grad`.
    """
    # TODO: Update both running averages exactly as in Theory.
    pass
