import numpy as np


def td_convergence_analysis(episodes, true_values, gamma, alpha):
    """
    Analyze TD(0) convergence.

    Args:
        episodes: list of episodes, each is a list of (state, reward, next_state) tuples
        true_values: dict {state: true_value}
        gamma: discount factor
        alpha: learning rate

    Returns:
        V_estimates: dict {state: estimated_value}
        mse_per_episode: list of MSE values after each episode
    """
    V = {}
    mse_per_episode = []

    for episode in episodes:
        # Run TD(0) for this episode
        for state, reward, next_state in episode:
            v_s = V.get(state, 0.0)
            v_s_prime = V.get(next_state, 0.0)

            td_error = reward + gamma * v_s_prime - v_s
            V[state] = v_s + alpha * td_error

        # Compute MSE after this episode
        mse = 0.0
        count = 0
        for state in true_values:
            v_est = V.get(state, 0.0)
            v_true = true_values[state]
            mse += (v_est - v_true) ** 2
            count += 1

        if count > 0:
            mse /= count

        mse_per_episode.append(mse)

    return V, mse_per_episode
