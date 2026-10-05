import numpy as np


def double_q_learning(env_step, num_episodes, epsilon, gamma, alpha, seed=None):
    """
    Double Q-Learning off-policy TD control.

    Args:
        env_step: function(state, action) -> (next_state, reward, done)
        num_episodes: number of episodes
        epsilon: exploration rate
        gamma: discount factor
        alpha: learning rate
        seed: random seed

    Returns:
        Q: dict {(state, action): estimated_value}
        policy: dict {state: best_action}
    """
    rng = np.random.default_rng(seed)

    Q1 = {}
    Q2 = {}

    def epsilon_greedy(Q, state):
        """Epsilon-greedy action selection."""
        if rng.random() < 1 - epsilon:
            actions = [0, 1, 2, 3]
            q_vals = [Q.get((state, a), 0.0) for a in actions]
            return int(np.argmax(q_vals))
        else:
            return rng.integers(0, 4)

    for _ in range(num_episodes):
        state = 0
        done = False

        while not done:
            action = epsilon_greedy(Q1, state)
            next_state, reward, done = env_step(state, action)

            # Decide which Q to update
            if rng.random() < 0.5:
                # Update Q1 using Q2 for evaluation
                best_action = int(np.argmax([Q1.get((next_state, a), 0.0) for a in range(4)]))
                q_val = Q2.get((next_state, best_action), 0.0)

                q_s_a = Q1.get((state, action), 0.0)
                td_error = reward + gamma * q_val - q_s_a
                Q1[(state, action)] = q_s_a + alpha * td_error
            else:
                # Update Q2 using Q1 for evaluation
                best_action = int(np.argmax([Q2.get((next_state, a), 0.0) for a in range(4)]))
                q_val = Q1.get((next_state, best_action), 0.0)

                q_s_a = Q2.get((state, action), 0.0)
                td_error = reward + gamma * q_val - q_s_a
                Q2[(state, action)] = q_s_a + alpha * td_error

            state = next_state

    # Average Q values
    Q = {}
    all_sa = set(Q1.keys()) | set(Q2.keys())
    for (s, a) in all_sa:
        Q[(s, a)] = (Q1.get((s, a), 0.0) + Q2.get((s, a), 0.0)) / 2

    # Build policy
    policy = {}
    for s in range(100):
        q_vals = [Q.get((s, a), 0.0) for a in range(4)]
        if max(q_vals) > -float('inf'):
            policy[s] = int(np.argmax(q_vals))

    return Q, policy
