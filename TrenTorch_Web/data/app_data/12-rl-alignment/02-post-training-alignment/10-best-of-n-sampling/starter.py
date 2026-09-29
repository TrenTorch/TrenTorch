import numpy as np


def best_of_n_select(responses: list, rewards: list) -> tuple:
    """
    Best-of-N is an INFERENCE-time strategy (unlike
    09-rejection-sampling-finetuning's training-time filtering): given
    N already-sampled responses and their reward-model scores, just
    return the single highest-scoring one to actually show the user.
    Returns (best_response, best_reward).
    """
    # TODO: best_index = argmax(rewards). Return (responses[best_index],
    # float(rewards[best_index])).
    pass


def expected_best_of_n_reward(reward_pool: np.ndarray, n: int, num_trials: int, seed: int = 0) -> float:
    """
    Monte-Carlo estimate of the EXPECTED reward of best-of-n sampling:
    repeatedly draw n samples (with replacement) from reward_pool,
    take the max of each draw, and average those maxes over
    num_trials repetitions. Demonstrates best-of-n's real, diminishing-
    returns shape: bigger n helps, but by less and less each time.
    """
    # TODO: use an rng = np.random.default_rng(seed). For num_trials
    # trials, rng.choice(reward_pool, size=n, replace=True), take
    # .max(), collect all the trial maxes, return their mean.
    pass
