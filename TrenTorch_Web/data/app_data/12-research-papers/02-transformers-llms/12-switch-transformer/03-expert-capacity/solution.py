import math


def expert_capacity(n_tokens, n_experts, capacity_factor):
    return math.ceil(capacity_factor * n_tokens / n_experts)
