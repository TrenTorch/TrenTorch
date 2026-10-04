def evaluate_state_value(trajectories, state, gamma):
    """
    Estimate the expected value (expected discounted return) of a state.

    Args:
        trajectories: list of trajectories, each is a list of (state, reward) tuples.
                     The reward is the reward received FOR entering that state.
        state: the target state (hashable)
        gamma: discount factor

    Returns:
        float: average discounted return starting from first visit to state
    """
    pass
