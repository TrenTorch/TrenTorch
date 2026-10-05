def estimate_state_values_every_visit(episodes, gamma):
    """
    Estimate state values using every-visit Monte Carlo.

    Args:
        episodes: list of episodes, each is a list of (state, reward) tuples
        gamma: discount factor

    Returns:
        dict mapping state -> estimated value
    """
    returns_dict = {}

    for episode in episodes:
        # Compute returns from every visit (not just first)
        for i, (state, _) in enumerate(episode):
            discounted_return = 0.0
            for k, (_, reward) in enumerate(episode[i:]):
                discounted_return += (gamma ** k) * reward

            if state not in returns_dict:
                returns_dict[state] = []
            returns_dict[state].append(discounted_return)

    value_dict = {}
    for state, returns in returns_dict.items():
        value_dict[state] = sum(returns) / len(returns)

    return value_dict
