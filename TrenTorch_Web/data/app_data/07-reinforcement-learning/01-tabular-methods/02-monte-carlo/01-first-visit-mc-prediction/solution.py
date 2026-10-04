def estimate_state_values(episodes, gamma):
    """
    Estimate state values using first-visit Monte Carlo.

    Args:
        episodes: list of episodes, each is a list of (state, reward) tuples
        gamma: discount factor

    Returns:
        dict mapping state -> estimated value
    """
    returns_dict = {}  # {state: [list of returns]}

    for episode in episodes:
        visited_states = set()
        # Compute returns from each first visit
        for i, (state, _) in enumerate(episode):
            if state not in visited_states:
                # First visit to this state in this episode
                visited_states.add(state)
                # Compute discounted return from this point onward
                discounted_return = 0.0
                for k, (_, reward) in enumerate(episode[i:]):
                    discounted_return += (gamma ** k) * reward

                # Store the return
                if state not in returns_dict:
                    returns_dict[state] = []
                returns_dict[state].append(discounted_return)

    # Average returns for each state
    value_dict = {}
    for state, returns in returns_dict.items():
        value_dict[state] = sum(returns) / len(returns)

    return value_dict
