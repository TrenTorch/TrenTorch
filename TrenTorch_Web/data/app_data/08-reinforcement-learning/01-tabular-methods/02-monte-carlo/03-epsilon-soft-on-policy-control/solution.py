import numpy as np


def epsilon_soft_mc_control(env_step, num_episodes, epsilon, gamma, seed=None):
    """
    Epsilon-soft on-policy MC control.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes to run
        epsilon: exploration probability
        gamma: discount factor
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: best_action}
    """
    rng = np.random.default_rng(seed)

    Q = {}  # (state, action) -> list of returns
    counts = {}  # (state, action) -> count
    actions_per_state = {}  # state -> set of actions

    for _ in range(num_episodes):
        episode = []
        state = 0  # Assume start state is 0
        done = False

        # Generate episode
        while not done:
            # Collect available actions
            if state not in actions_per_state:
                actions_per_state[state] = set()

            # Epsilon-soft action selection
            if state in Q and len(actions_per_state[state]) > 0:
                # Pick best action w.p. 1-ε
                valid_actions = list(actions_per_state[state])
                q_values = [Q.get((state, a), 0.0) for a in valid_actions]
                best_action = valid_actions[np.argmax(q_values)]

                if rng.random() < 1 - epsilon:
                    action = best_action
                else:
                    action = rng.choice(valid_actions)
            else:
                # Random action
                action = 0

            # Take step
            next_state, reward, done = env_step(state, action)
            episode.append((state, action, reward))

            # Track actions seen
            actions_per_state[state].add(action)

            state = next_state

        # Compute returns and update Q
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = r + gamma * G

            if (s, a) not in Q:
                Q[(s, a)] = []
                counts[(s, a)] = 0

            Q[(s, a)].append(G)
            counts[(s, a)] += 1

    # Average returns
    Q_avg = {}
    for (s, a), returns in Q.items():
        Q_avg[(s, a)] = sum(returns) / len(returns)

    # Build greedy policy
    policy = {}
    for state in actions_per_state:
        valid_actions = list(actions_per_state[state])
        q_vals = [Q_avg.get((state, a), 0.0) for a in valid_actions]
        policy[state] = valid_actions[np.argmax(q_vals)]

    return Q_avg, policy
