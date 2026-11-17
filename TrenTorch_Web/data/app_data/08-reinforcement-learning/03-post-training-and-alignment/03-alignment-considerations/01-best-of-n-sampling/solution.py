import numpy as np


def best_of_n_select(responses: list, rewards: list) -> tuple:
    rewards = np.asarray(rewards, dtype=float)
    best_index = int(np.argmax(rewards))
    return responses[best_index], float(rewards[best_index])


def expected_best_of_n_reward(reward_pool: np.ndarray, n: int, num_trials: int, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    reward_pool = np.asarray(reward_pool, dtype=float)
    best_rewards = np.empty(num_trials)
    for trial in range(num_trials):
        sample = rng.choice(reward_pool, size=n, replace=True)
        best_rewards[trial] = sample.max()
    return float(best_rewards.mean())
