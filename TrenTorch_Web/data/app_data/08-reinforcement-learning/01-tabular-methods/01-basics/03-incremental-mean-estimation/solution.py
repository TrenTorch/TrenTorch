def update_incremental_mean(estimate, count, reward):
    """
    Update mean estimate incrementally.

    Args:
        estimate: current mean Q_n (from n samples)
        count: number of samples seen so far (n, before this reward)
        reward: new reward R_{n+1}

    Returns:
        float: updated mean Q_{n+1}
    """
    return estimate + (1.0 / (count + 1)) * (reward - estimate)
