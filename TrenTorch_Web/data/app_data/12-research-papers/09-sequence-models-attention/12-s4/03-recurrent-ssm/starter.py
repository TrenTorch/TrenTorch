def recurrent_ssm(A_bar, B_bar, C, x):
    """
    A_bar, B_bar, C: scalar discrete system parameters
    x: input sequence

    Returns:
        The output sequence y_t = C h_t, where h_t = A_bar h_{t-1} + B_bar x_t and h_{-1} = 0.
    """
    # TODO: Run the state recurrence and read out the output at each step (see Theory).
    pass
