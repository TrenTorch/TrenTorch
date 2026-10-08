def overestimation_gap(max_target_q, double_target):
    """
    max_target_q: the standard DQN target's value (max over the target network)
    double_target: the Double DQN target's value for the same transition

    Returns:
        The gap max_target_q - double_target, positive when the standard target overestimates.
    """
    # TODO: Subtract the Double DQN target from the standard max target (see Theory).
    pass
