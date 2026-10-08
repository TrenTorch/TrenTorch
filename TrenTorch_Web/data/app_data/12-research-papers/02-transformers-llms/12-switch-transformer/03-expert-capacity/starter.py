import math


def expert_capacity(n_tokens, n_experts, capacity_factor):
    """
    n_tokens: tokens in the batch
    n_experts: number of experts
    capacity_factor: slack multiplier (1.0 means exactly the average load)

    Returns:
        The number of tokens each expert can process: ceil(capacity_factor * n_tokens / n_experts).
    """
    # TODO: Compute the per-expert capacity from Theory and return it as an integer.
    pass
