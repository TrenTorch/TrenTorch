def kl_penalized_reward(reward, logp_policy, logp_ref, beta):
    return reward - beta * (logp_policy - logp_ref)
