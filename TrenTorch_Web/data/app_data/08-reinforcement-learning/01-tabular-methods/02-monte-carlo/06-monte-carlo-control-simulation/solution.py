import numpy as np


def mc_control_gridworld(num_episodes, epsilon, gamma, seed=None):
    """
    Run MC control on a simple 4x4 gridworld.

    Args:
        num_episodes: number of episodes to run
        epsilon: exploration rate
        gamma: discount factor
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: action}
        episode_rewards: list of cumulative rewards per episode
    """
    rng = np.random.default_rng(seed)

    # Gridworld setup
    goal = (3, 3)
    max_steps = 50

    def step(state, action):
        r, c = state
        # Actions: 0=N, 1=S, 2=E, 3=W
        if action == 0:  # North
            r = max(0, r - 1)
        elif action == 1:  # South
            r = min(3, r + 1)
        elif action == 2:  # East
            c = min(3, c + 1)
        elif action == 3:  # West
            c = max(0, c - 1)

        next_state = (r, c)
        done = next_state == goal
        reward = 10.0 if done else -1.0

        return next_state, reward, done

    Q = {}
    returns_dict = {}
    episode_rewards = []

    for episode_num in range(num_episodes):
        episode = []
        state = (0, 0)
        done = False
        step_count = 0

        # Generate episode
        while not done and step_count < max_steps:
            # Epsilon-soft action selection
            if rng.random() < 1 - epsilon:
                # Greedy: choose best action
                q_vals = [Q.get((state, a), 0.0) for a in range(4)]
                action = int(np.argmax(q_vals))
            else:
                # Explore: random action
                action = rng.integers(0, 4)

            next_state, reward, done = step(state, action)
            episode.append((state, action, reward))
            state = next_state
            step_count += 1

        # Compute returns and update Q
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = r + gamma * G

            if (s, a) not in returns_dict:
                returns_dict[(s, a)] = []
            returns_dict[(s, a)].append(G)

        # Average returns
        for (s, a), returns in returns_dict.items():
            Q[(s, a)] = np.mean(returns)

        # Track episode reward
        episode_rewards.append(sum(r for _, _, r in episode))

    # Build policy
    policy = {}
    for state in [(r, c) for r in range(4) for c in range(4)]:
        q_vals = [Q.get((state, a), 0.0) for a in range(4)]
        policy[state] = int(np.argmax(q_vals))

    return Q, policy, episode_rewards
