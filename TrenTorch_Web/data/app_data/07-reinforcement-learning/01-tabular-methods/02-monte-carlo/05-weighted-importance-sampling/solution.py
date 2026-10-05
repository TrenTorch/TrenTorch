def estimate_weighted_importance_sampling(episodes, gamma):
    """
    Estimate off-policy returns using weighted importance sampling.

    Args:
        episodes: list of episodes, each is a list of (state, action, reward) tuples
        gamma: discount factor

    Returns:
        dict {(state, action): estimated_value}
    """
    numerator = {}  # (state, action) -> sum of W_t * G_t
    denominator = {}  # (state, action) -> sum of W_t

    for episode in episodes:
        # Compute returns
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = r + gamma * G

            # Collect unique actions in episode for behavior policy
            actions_in_episode = set(x[1] for x in episode)
            num_actions = len(actions_in_episode)

            # Compute importance weight from t onward
            W = 1.0
            for i in range(t, len(episode)):
                s_i, a_i, _ = episode[i]

                # β(a|s) = 1 / num_actions (uniform)
                beta_prob = 1.0 / num_actions if a_i in actions_in_episode else 0.0

                # π(a|s) = greedy (1.0 for best action, 0.0 for others)
                q_vals = {s_i: sum(
                    numerator.get((s_i, a), 0.0) / max(denominator.get((s_i, a), 1), 1)
                    for a in actions_in_episode
                )}
                best_action = max(actions_in_episode, key=lambda x: numerator.get((s_i, x), 0.0) / max(denominator.get((s_i, x), 1), 1))
                pi_prob = 1.0 if a_i == best_action else 0.0

                if beta_prob > 0:
                    W *= pi_prob / beta_prob
                else:
                    W = 0.0
                    break

            # Accumulate weighted return
            if W > 0:
                if (s, a) not in numerator:
                    numerator[(s, a)] = 0.0
                    denominator[(s, a)] = 0.0

                numerator[(s, a)] += W * G
                denominator[(s, a)] += W

    # Compute weighted average
    result = {}
    for (s, a) in numerator:
        if denominator[(s, a)] > 0:
            result[(s, a)] = numerator[(s, a)] / denominator[(s, a)]
        else:
            result[(s, a)] = 0.0

    return result
