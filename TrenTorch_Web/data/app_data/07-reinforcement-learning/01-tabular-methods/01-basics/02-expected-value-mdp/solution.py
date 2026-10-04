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
    returns = []

    for trajectory in trajectories:
        # Find first visit to the target state
        first_visit_idx = None
        for i, (s, _) in enumerate(trajectory):
            if s == state:
                first_visit_idx = i
                break

        # If state not found in this trajectory, skip it
        if first_visit_idx is None:
            continue

        # Compute discounted return from first visit onward
        discounted_return = 0.0
        for k, (_, reward) in enumerate(trajectory[first_visit_idx:]):
            discounted_return += (gamma ** k) * reward

        returns.append(discounted_return)

    # Return average, or 0.0 if no visits
    if len(returns) == 0:
        return 0.0
    return sum(returns) / len(returns)
