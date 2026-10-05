import numpy as np


def expected_sarsa(env_step, num_episodes, epsilon, gamma, alpha, seed=None):
    """
    Expected SARSA on-policy TD control.

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
    num_actions = 4

    def epsilon_greedy(state):
        """Epsilon-greedy action selection."""
        if rng.random() < 1 - epsilon:
            actions = list(range(num_actions))
            q_vals = [Q.get((state, a), 0.0) for a in actions]
            return int(np.argmax(q_vals))
        else:
            return rng.integers(0, num_actions)

    def expected_q_value(state):
        """Compute expected Q value under epsilon-greedy policy."""
        q_vals = [Q.get((state, a), 0.0) for a in range(num_actions)]
        max_q = max(q_vals)
        sum_q = sum(q_vals)

        expected = (1 - epsilon) * max_q + (epsilon / num_actions) * sum_q
        return expected

    for _ in range(num_episodes):
        state = 0
        done = False

        while not done:
            action = epsilon_greedy(state)
            next_state, reward, done = env_step(state, action)

            # Expected SARSA: use expected value of next state
            exp_q_next = expected_q_value(next_state)

            q_s_a = Q.get((state, action), 0.0)
            td_error = reward + gamma * exp_q_next - q_s_a
            Q[(state, action)] = q_s_a + alpha * td_error

            state = next_state

    # Build policy
    policy = {}
    for s in range(100):
        q_vals = [Q.get((s, a), 0.0) for a in range(num_actions)]
        if max(q_vals) > -float('inf'):
            policy[s] = int(np.argmax(q_vals))

    return Q, policy
