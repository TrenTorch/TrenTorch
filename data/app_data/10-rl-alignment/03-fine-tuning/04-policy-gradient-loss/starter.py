import numpy as np


def discounted_returns(rewards: np.ndarray, gamma: float, dones: np.ndarray) -> np.ndarray:
    """
    The REINFORCE return at each timestep t: the sum of all rewards
    from t onward, each discounted by gamma^k (k steps into the
    future), reset to zero whenever an episode boundary (`dones[t]`)
    is crossed. Computed efficiently via a single backward pass:
    G[t] = rewards[t] + gamma * (1 - dones[t]) * G[t+1].
    """
    # TODO: loop t from the LAST index down to 0, maintaining a running
    # total: running = rewards[t] + gamma * (1 - dones[t]) * running.
    # Store running into returns[t] each step. Start running at 0.0.
    pass


def policy_gradient_loss(log_probs: np.ndarray, advantages: np.ndarray) -> float:
    """
    The basic REINFORCE policy-gradient loss: -mean(log_prob *
    advantage) -- pushes UP the log-probability of actions with a
    positive advantage (better than expected) and DOWN actions with a
    negative advantage, exactly the same shape GRPO's loss uses, just
    with `advantages` here potentially being raw discounted_returns
    (no baseline subtraction) rather than a group-normalized advantage.
    """
    # TODO: -np.mean(log_probs * advantages)
    pass
