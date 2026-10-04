import numpy as np


def mc_exploring_starts(env_step, num_episodes, gamma, num_states=10, num_actions=4, seed=None):
    """
    Monte Carlo control with exploring starts.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes to run
        gamma: discount factor
        num_states: number of possible states
        num_actions: number of possible actions
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: best_action}
    """
    rng = np.random.default_rng(seed)

    Q = {}  # (state, action) -> list of returns
    returns_dict = {}
    policy = {}  # state -> action

    for _ in range(num_episodes):
        # Random start state and action
        start_state = rng.integers(0, num_states)
        start_action = rng.integers(0, num_actions)

        episode = []
        state = start_state
        action = start_action
        done = False
        step_count = 0
        max_steps = 100

        # Take first action
        next_state, reward, done = env_step(state, action)
        episode.append((state, action, reward))
        state = next_state
        step_count += 1

        # Follow greedy policy
        while not done and step_count < max_steps:
            # Choose greedy action
            if state in policy:
                action = policy[state]
            else:
                # No policy yet, take random action
                action = rng.integers(0, num_actions)

            next_state, reward, done = env_step(state, action)
            episode.append((state, action, reward))
            state = next_state
            step_count += 1

        # Update Q with first-visit MC
        visited = set()
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = r + gamma * G

            if (s, a) not in visited:
                visited.add((s, a))

                if (s, a) not in returns_dict:
                    returns_dict[(s, a)] = []
                returns_dict[(s, a)].append(G)
                Q[(s, a)] = np.mean(returns_dict[(s, a)])

        # Update policy
        for state in range(num_states):
            q_vals = [Q.get((state, a), 0.0) for a in range(num_actions)]
            policy[state] = int(np.argmax(q_vals))

    return Q, policy
