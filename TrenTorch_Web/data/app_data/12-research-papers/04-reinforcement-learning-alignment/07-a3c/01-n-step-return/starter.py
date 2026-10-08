def n_step_return(rewards, bootstrap, gamma):
    """
    rewards: the n rewards collected in the rollout, in time order
    bootstrap: value estimate of the state after the last reward (0 if terminal)
    gamma: discount factor

    Returns:
        The n-step return r_0 + gamma r_1 + ... + gamma^(n-1) r_(n-1) + gamma^n bootstrap, as a float.
    """
    # TODO: Start from the bootstrap value and fold in each reward from the end backward (see Theory).
    pass
