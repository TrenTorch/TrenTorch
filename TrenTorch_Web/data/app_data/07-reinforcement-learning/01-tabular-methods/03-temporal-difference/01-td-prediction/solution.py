def td_prediction(episodes, gamma, alpha):
    """
    TD(0) prediction.

    Args:
        episodes: list of episodes, each is a list of (state, reward, next_state) tuples
        gamma: discount factor
        alpha: learning rate

    Returns:
        dict {state: estimated_value}
    """
    V = {}  # state -> value

    for episode in episodes:
        for state, reward, next_state in episode:
            # Get current values
            v_s = V.get(state, 0.0)
            v_s_prime = V.get(next_state, 0.0)

            # Compute TD error
            td_error = reward + gamma * v_s_prime - v_s

            # Update value
            V[state] = v_s + alpha * td_error

    return V
