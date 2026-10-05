import numpy as np


def q_learning(env_step, num_episodes, epsilon, gamma, alpha, seed=None):
    """
    Q-Learning off-policy TD control.

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
            actions = [0, 1, 2, 3]
            q_vals = [Q.get((state, a), 0.0) for a in actions]
            return int(np.argmax(q_vals))
        else:
            # Random
            return rng.integers(0, 4)

    for _ in range(num_episodes):
        state = 0
        done = False

        while not done:
            action = epsilon_greedy(state)
            next_state, reward, done = env_step(state, action)

            # Q-learning: use max Q(s',a') for all a'
            max_q_next = max([Q.get((next_state, a), 0.0) for a in range(4)])

            q_s_a = Q.get((state, action), 0.0)
            td_error = reward + gamma * max_q_next - q_s_a
            Q[(state, action)] = q_s_a + alpha * td_error

            state = next_state

    # Build policy
    policy = {}
    for s in range(100):
        q_vals = [Q.get((s, a), 0.0) for a in range(4)]
        if max(q_vals) > -float('inf'):
            policy[s] = int(np.argmax(q_vals))

    return Q, policy
