def ssm_kernel(A_bar, B_bar, C, L):
    """
    A_bar, B_bar, C: scalar discrete system parameters
    L: kernel length

    Returns:
        The length-L impulse response K_k = C A_bar^k B_bar, for k = 0 .. L-1.
    """
    # TODO: Compute C * A_bar^k * B_bar for each lag k (see Theory).
    pass
