def act_remainder(halts):
    """
    halts: halting probabilities p_1, ..., p_N for the steps taken, with the last one not yet final

    Returns:
        The remainder 1 - sum(p_1 .. p_{N-1}), the weight given to the final step.
    """
    # TODO: Subtract the probabilities of all but the last step from one (see Theory).
    pass
