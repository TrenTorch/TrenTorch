def estimate_off_policy_returns(episodes, gamma):
    """
    Estimate off-policy returns using importance sampling.

    Args:
        episodes: list of episodes, each is a list of (state, action, reward) tuples
        gamma: discount factor

    Returns:
        dict {(state, action): estimated_value}
    """
    Q = {}  # (state, action) -> list of weighted returns
    def mean_q(s, a):
        returns = Q.get((s, a))
        return sum(returns) / len(returns) if returns else 0.0


    for episode in episodes:
        # Compute returns
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = r + gamma * G

            # Compute importance weight from t onward
            # Assume behavior policy β is uniform over actions seen in episode
            # Target policy π is greedy w.r.t. Q
            actions_in_episode = set(x[1] for x in episode)
            num_actions = len(actions_in_episode)

            W = 1.0
            for i in range(t, len(episode)):
                s_i, a_i, _ = episode[i]

                # β(a|s) = 1 / num_actions (uniform over observed actions)
                beta_prob = 1.0 / num_actions if a_i in actions_in_episode else 0.0

                # π(a|s) - greedy: 1.0 if a is best, 0.0 otherwise
                # For simplicity, assume π is deterministic greedy
                best_action = max(actions_in_episode, key=lambda x: mean_q(s_i, x))
                pi_prob = 1.0 if a_i == best_action else 0.0

                if beta_prob > 0:
                    W *= pi_prob / beta_prob
                else:
                    W = 0.0
                    break

            # Store weighted return
            if W > 0:
                if (s, a) not in Q:
                    Q[(s, a)] = []
                Q[(s, a)].append(W * G)

    # Average weighted returns
    result = {}
    for (s, a), weighted_returns in Q.items():
        result[(s, a)] = sum(weighted_returns) / len(weighted_returns) if weighted_returns else 0.0

    return result
