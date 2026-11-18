def bias_corrected(m, v, beta1, beta2, t):
    """
    m, v: raw first and second moment estimates
    beta1, beta2: decay rates; t: step count starting at 1

    Returns:
        The bias-corrected pair (m_hat, v_hat) as Python floats.
    """
    # TODO: Divide each moment by one minus its decay raised to the step count (see Theory).
    pass
