def kl_penalized_reward(reward, logp_policy, logp_ref, beta):
    """
    reward: reward model score for the sampled response
    logp_policy: log-probability of the response under the policy being trained
    logp_ref: log-probability of the same response under the frozen reference model
    beta: strength of the penalty

    Returns:
        reward - beta * (logp_policy - logp_ref).
    """
    # TODO: Subtract beta times the log-ratio from the reward (see Theory).
    pass
