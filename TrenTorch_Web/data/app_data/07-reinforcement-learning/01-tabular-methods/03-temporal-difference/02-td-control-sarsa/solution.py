import numpy as np


def sarsa(env_step, num_episodes, epsilon, gamma, alpha, seed=None):
    """
    SARSA on-policy TD control.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes
        epsilon: exploration rate
        gamma: discount factor
        alpha: learning rate
        seed: random seed

    Returns:
        Q: dict {(state, action): value}
        policy: dict {state: best_action}
    """
    rng = np.random.default_rng(seed)

    Q = {}

    def epsilon_greedy(state):
        """Select action epsilon-greedy."""
        if rng.random() < 1 - epsilon:
            # Greedy
            actions = [0, 1, 2, 3]  # 4 actions
            q_vals = [Q.get((state, a), 0.0) for a in actions]
            return int(np.argmax(q_vals))
        else:
            # Random
            return rng.integers(0, 4)

    for _ in range(num_episodes):
        state = 0
        action = epsilon_greedy(state)
        done = False

        while not done:
            next_state, reward, done = env_step(state, action)
            next_action = epsilon_greedy(next_state)

            # SARSA update
            q_s_a = Q.get((state, action), 0.0)
            q_s_prime_a_prime = Q.get((next_state, next_action), 0.0)

            td_error = reward + gamma * q_s_prime_a_prime - q_s_a
            Q[(state, action)] = q_s_a + alpha * td_error

            state = next_state
            action = next_action

    # Build policy
    policy = {}
    for s in range(100):  # Assume up to 100 states
        q_vals = [Q.get((s, a), 0.0) for a in range(4)]
        if max(q_vals) > -float('inf'):
            policy[s] = int(np.argmax(q_vals))

    return Q, policy
